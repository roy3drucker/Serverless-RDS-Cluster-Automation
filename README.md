# Serverless RDS Cluster Automation

This project provides an automated solution for provisioning RDS clusters on AWS using a Serverless architecture and Infrastructure as Code.

## Architecture

1. **API Gateway**: Entry point for provisioning requests.
2. **SNS & SQS**: Decouples the request from processing, ensuring reliability.
3. **Lambda**: Consumes messages, generates Terraform code, and creates a GitHub Pull Request.
4. **Terraform**: Defines the RDS infrastructure.
5. **CircleCI**: Orchestrates the deployment of the serverless stack and the application of Terraform changes.

## Prerequisites

- AWS Account
- GitHub Account & Personal Access Token (PAT) with `repo` scope.
- CircleCI Account linked to GitHub.
- AWS Credentials configured in CircleCI (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION).
- GitHub PAT stored in AWS Secrets Manager (Secret Name: `github/pat` by default).

## Deployment

### 1. Initial Setup

1. Fork/Clone this repository.
2. Store your GitHub PAT in AWS Secrets Manager:
   ```bash
   aws secretsmanager create-secret --name github/pat --secret-string "YOUR_GITHUB_TOKEN".
   ```
3. Push the code to GitHub.
4. Set up the project in CircleCI.

### 2. Serverless Stack Deployment

The `deploy-serverless` job in CircleCI will automatically deploy the API Gateway, Lambda, SNS, and SQS stack when you push to `main`.

Alternatively, you can deploy manually using AWS SAM:
```bash
sam build
sam deploy --guided
```

## Usage

To provision a new RDS cluster, send a POST request to the API Gateway endpoint (outputted by the SAM deployment).

**Endpoint:** `https://<api-id>.execute-api.<region>.amazonaws.com/Prod/provision`

**Payload:**
```json
{
  "db_name": "my-app-db",
  "engine": "mysql",
  "environment": "dev"
}
```

### What happens next?

1. The request is queued in SQS.
2. The Lambda function picks it up.
3. A new branch `feature/provision-rds-my-app-db` is created in this repo.
4. A Terraform file `terraform/live/my-app-db.tf` is added.
5. A Pull Request is opened against `main`.
6. CircleCI runs `terraform plan` on the PR.
7. Once you merge the PR, CircleCI runs `terraform apply` to create the RDS database.

## Directory Structure

- `lambda/`: Python source code for the Lambda function.
- `terraform/modules/rds/`: Terraform module for the RDS cluster.
- `template.yaml`: AWS SAM template.
- `.circleci/`: CI/CD configuration.
