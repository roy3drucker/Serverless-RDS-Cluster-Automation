# Variables are defined in main.tf for this simple module, 
# but usually we split them. Since I put them in main.tf above, 
# I will create a dummy outputs.tf or just skip this if not strictly needed.
# Let's actually move variables to variables.tf to be cleaner.

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
