provider "aws" {
  region     = "eu-west-2"
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

# Lambda for pipeline and dashboard

# EventBridge for pipeline and dashboard

# ECS Fargate for transfer script

# S3 bucket for the long term storage of the data
resource "aws_s3_bucket" "example" {
  bucket = "my-tf-test-bucket"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}
