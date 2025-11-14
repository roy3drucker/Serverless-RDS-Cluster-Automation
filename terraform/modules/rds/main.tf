data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.database_name}-${var.environment}"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_security_group" "rds" {
  name   = "${var.database_name}-${var.environment}-rds"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port   = var.engine == "mysql" ? 3306 : 5432
    to_port     = var.engine == "mysql" ? 3306 : 5432
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.default.cidr_block]
  }
}

resource "random_password" "master" {
  length = 16
}

resource "aws_secretsmanager_secret" "password" {
  name = "${var.database_name}-${var.environment}-password"
}

resource "aws_secretsmanager_secret_version" "password" {
  secret_id     = aws_secretsmanager_secret.password.id
  secret_string = random_password.master.result
}

resource "aws_db_instance" "main" {
  identifier = "${var.database_name}-${var.environment}"
  
  engine         = var.engine
  engine_version = var.engine == "mysql" ? "8.0" : "15"
  instance_class = var.instance_class
  
  allocated_storage = 20
  storage_encrypted = true
  
  db_name  = var.database_name
  username = "admin"
  password = random_password.master.result
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  skip_final_snapshot = true
}