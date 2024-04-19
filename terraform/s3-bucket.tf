resource "aws_s3_bucket" "long_term_storage_bucket" {
  bucket = "cretaceous-paleogene"

  tags = {
    Name        = "Long Term Storage Bucket"
    Environment = "Dev"
  }
}


