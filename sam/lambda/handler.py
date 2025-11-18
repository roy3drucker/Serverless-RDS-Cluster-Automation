import json
import os
import logging
from github import Github

# CloudWatch logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Processing {len(event['Records'])} records")
    
    github = Github(os.environ['GITHUB_TOKEN'])
    repo = github.get_repo(f"roy3drucker/{os.environ['GITHUB_REPO']}")
    
    for record in event['Records']:
        try:
            # Parse message
            message = json.loads(record['body'])
            data = json.loads(message['Message'])
            
            db_name = data['database_name']
            engine = data['engine']
            environment = data['environment']
            
            logger.info(f"Creating RDS: {db_name} ({engine}, {environment})")
            
            # Generate Terraform
            terraform_content = f'''module "rds_{db_name}" {{
  source = "../terraform/modules/rds"
  
  database_name = "{db_name}"
  engine = "{engine}"
  environment = "{environment}"
  instance_class = "{"db.t3.micro" if environment == "dev" else "db.t3.small"}"
}}

output "{db_name}_endpoint" {{
  value = module.rds_{db_name}.endpoint
}}'''
            
            # Create GitHub PR
            branch_name = f"rds-{db_name}-{environment}"
            file_path = f"terraform-instances/{db_name}-{environment}.tf"
            
            # Create branch
            main_branch = repo.get_branch("main")
            repo.create_git_ref(f"refs/heads/{branch_name}", main_branch.commit.sha)
            
            # Create file
            repo.create_file(
                path=file_path,
                message=f"Add RDS {db_name}",
                content=terraform_content,
                branch=branch_name
            )
            
            # Create PR
            pr = repo.create_pull(
                title=f"Deploy RDS: {db_name} ({environment})",
                body=f"Auto-generated PR for {db_name} RDS cluster",
                head=branch_name,
                base="main"
            )
            
            logger.info(f"Created PR: {pr.html_url}")
            
        except Exception as e:
            logger.error(f"Error: {e}")
    
    return {'statusCode': 200}
