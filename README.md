# Serverless RDS Cluster Automation

## 🚀 Overview

This project provides a fully automated, serverless solution to provision **AWS RDS clusters on-demand** using Infrastructure as Code (IaC) and CI/CD best practices.

Developers can request a new RDS cluster by submitting a POST request to an API Gateway endpoint with a JSON payload specifying:
- Database Name
- Database Engine (`MySQL` or `PostgreSQL`)
- Environment (`dev` or `prod`)

The system ensures:
- ✅ Decoupled and reliable processing via SNS and SQS
- ✅ Automatic infrastructure provisioning via Terraform
- ✅ GitHub PR generation by Lambda
- ✅ Fully automated deployment via CircleCI

---

## 🏗️ Architecture

The solution is built using the following components:

### **Serverless Stack (via AWS SAM)**
- **API Gateway** - Exposes `/request-rds` endpoint
- **SNS Topic** - Receives API requests
- **SQS Queue** - Buffers incoming requests
- **Lambda Function** - 
  - Consumes messages from SQS
  - Generates a GitHub Pull Request containing Terraform code for the requested RDS
  - Uses `boto3` and `PyGitHub`

### **Terraform Module**
- Defines the RDS cluster using configurable variables: DB name, engine, environment
- Chooses instance size based on environment (`t3.micro` for dev, `db.t3.medium` for prod)

### **CI/CD - CircleCI**
- Automates deployment of serverless resources (SAM)
- Applies Terraform changes when PR is merged
- Scheduled cleanup pipeline deletes old clusters (Bonus)

---

## 🚀 Deployment Instructions

### ✅ Prerequisites
- AWS account with programmatic access
- GitHub repository with PAT token
- CircleCI account connected to GitHub
- Enable required IAM permissions:
  - `cloudformation:*`, `lambda:*`, `apigateway:*`, `sns:*`, `sqs:*`, `iam:*`, `rds:*`

### 1. Clone this repository

```bash
git clone https://github.com/<your-username>/serverless-rds-cluster-automation.git
cd serverless-rds-cluster-automation


### **Setup Environment Variables in CircleCI**

In your CircleCI project settings, add the following environment variables:

Variable	Description
AWS_ACCESS_KEY_ID	AWS access key
AWS_SECRET_ACCESS_KEY	AWS secret
AWS_REGION	e.g., us-east-1
GITHUB_TOKEN	GitHub Personal Access Token
GITHUB_REPO	e.g., yourusername/reponame
ENV	dev or prod (stage name)

### Deploy the Serverless Stack:
Deployment is automated via CircleCI when you merged your PR to the main branch.

### How to Use the Automation
Step 1: Submit an RDS Provisioning Request

Send a POST request to the API Gateway endpoint (provided in SAM outputs):
POST /request-rds
Host: <your-api-id>.execute-api.<region>.amazonaws.com/<stage>
Headers:
  x-api-key: <your-api-key>
  Content-Type: application/json

Body:
{
  "db_name": "myappdb",
  "db_engine": "postgres",
  "environment": "dev"
}

Step 2: What Happens Next?
The request is published to SNS

SQS receives and buffers the message

- Lambda is triggered:
- Parses the request
- Creates a GitHub Pull Request with a Terraform file that provisions the RDS cluster
- You (or an approver) merge the PR
- CircleCI runs Terraform apply to provision the RDS instance

### 🧹 Bonus Features

✅ Auto-cleanup: Scheduled CircleCI job to delete unused RDS clusters
✅ API Key Authentication: API Gateway requires x-api-key for all requests
✅ Secure Parameter Handling: All secrets (GitHub token, DB credentials) passed as environment variables or stored securely

