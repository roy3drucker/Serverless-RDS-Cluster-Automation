import json
import os
import boto3
from github import Github

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise e

def generate_terraform_code(db_name, engine, environment):
    # In a real scenario, source would be a git url or relative path
    # We assume the module is in the same repo at terraform/modules/rds
    return f"""
module "rds_{db_name}" {{
  source      = "../modules/rds"
  db_name     = "{db_name}"
  engine      = "{engine}"
  environment = "{environment}"
}}
"""

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    github_repo_name = os.environ['GITHUB_REPO']
    secret_name = os.environ['GITHUB_SECRET_NAME']
    
    # Get GitHub Token
    github_token = get_secret(secret_name)
    g = Github(github_token)
    repo = g.get_repo(github_repo_name)
    
    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            db_name = body.get('db_name')
            engine = body.get('engine')
            environment = body.get('environment')
            
            if not all([db_name, engine, environment]):
                print("Missing required fields in message")
                continue
                
            branch_name = f"feature/provision-rds-{db_name}"
            file_path = f"terraform/live/{db_name}.tf"
            file_content = generate_terraform_code(db_name, engine, environment)
            commit_message = f"Provision RDS cluster: {db_name}"
            
            # Check if branch exists, if not create it from main
            try:
                repo.get_branch(branch_name)
                print(f"Branch {branch_name} already exists")
            except:
                source_branch = repo.get_branch("main")
                repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)
                print(f"Created branch {branch_name}")
            
            # Create or Update file
            try:
                contents = repo.get_contents(file_path, ref=branch_name)
                repo.update_file(contents.path, commit_message, file_content, contents.sha, branch=branch_name)
                print(f"Updated file {file_path}")
            except:
                repo.create_file(file_path, commit_message, file_content, branch=branch_name)
                print(f"Created file {file_path}")
                
            # Create Pull Request
            try:
                pr = repo.create_pull(
                    title=f"Provision RDS: {db_name}",
                    body=f"Automated PR to provision RDS cluster '{db_name}' ({engine}) in {environment}.",
                    head=branch_name,
                    base="main"
                )
                print(f"Created PR #{pr.number}: {pr.html_url}")
            except Exception as e:
                if "A pull request already exists" in str(e):
                    print("PR already exists")
                else:
                    raise e
                    
        except Exception as e:
            print(f"Error processing record: {e}")
            raise e
            
    return {'statusCode': 200, 'body': 'Processing complete'}
