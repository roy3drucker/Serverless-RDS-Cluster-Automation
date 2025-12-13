module "network" {
  source = "../modules/vpc"
}

module "rds" {
  source = "../modules/rds"

  db_name                = "mydatabase"
  engine                 = "mysql"
  environment            = "dev"
  
  # Pass network outputs to RDS module
  vpc_security_group_ids = module.network.vpc_security_group_ids
  db_subnet_group_name   = module.network.db_subnet_group_name
}
