# Variables are in variables.tf

locals {
  instance_class = var.environment == "prod" ? "db.t3.medium" : "db.t3.micro"
  allocated_storage = var.environment == "prod" ? 100 : 20
  # Determine engine version or family if needed, keeping it simple for now
}

resource "aws_db_instance" "default" {
  allocated_storage    = local.allocated_storage
  db_name              = var.db_name
  engine               = var.engine
  engine_version       = var.engine == "mysql" ? "8.0" : "13.7"
  instance_class       = local.instance_class
  username             = "admin"
  password             = "AvoidHardcodingPasswords123!" # In real world, use Secrets Manager
  parameter_group_name = "default.${var.engine}${var.engine == "mysql" ? "8.0" : "13"}"
  skip_final_snapshot  = true
  publicly_accessible  = false

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Note: For a real production setup, we would use aws_secretsmanager_secret for the password
# and likely an RDS Cluster (Aurora) for high availability in Prod.
# Keeping it simple for this assignment as per "Junior" level but following structure.
