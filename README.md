# RDS Provisioner

Simple automated RDS provisioning using AWS serverless architecture.

## Setup

1. **Create GitHub repo** and get Personal Access Token
2. **Setup CircleCI** with environment variables:
   ```
   AWS_ACCESS_KEY_ID
   AWS_SECRET_ACCESS_KEY
   GITHUB_TOKEN
   ```
3. **Edit handler.py** - replace `YOUR_USERNAME` with your GitHub username
4. **Push to main branch**

## Usage

Send POST request to API Gateway endpoint:

```bash
curl -X POST https://YOUR-API-ENDPOINT/prod/request-rds \
  -H "Content-Type: application/json" \
  -d '{
    "database_name": "myapp",
    "engine": "mysql",
    "environment": "dev"
  }'
```

## Flow

1. API Gateway → SNS → SQS → Lambda
2. Lambda creates GitHub PR with Terraform code
3. Merge PR → CircleCI deploys RDS

## Files

- `sam/template.yaml` - AWS infrastructure
- `sam/lambda/handler.py` - Lambda function
- `terraform/modules/rds/` - RDS module
- `.circleci/config.yml` - CI/CD pipeline

Total: ~200 lines of code