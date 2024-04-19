provider "aws" {
  region     = "eu-west-2"
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

resource "aws_s3_bucket" "long_term_storage_bucket" {
  bucket = "cretaceous-paleogene-terraform"

  tags = {
    Name        = "Long Term Storage Bucket"
    Environment = "Dev"
  }
}


