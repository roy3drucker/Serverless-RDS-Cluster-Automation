
module "rds_rds" {
  source      = "../modules/rds"
  db_name     = "rds"
  engine      = "mysql"
  environment = "production"
}
