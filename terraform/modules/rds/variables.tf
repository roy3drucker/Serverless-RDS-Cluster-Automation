variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "engine" {
  description = "Database engine (mysql, postgres)"
  type        = string
}

variable "environment" {
  description = "Environment (dev, prod)"
  type        = string
}

variable "vpc_security_group_ids" {
  description = "List of VPC Security Group IDs"
  type        = list(string)
}

variable "db_subnet_group_name" {
  description = "Name of the DB Subnet Group"
  type        = string
}
