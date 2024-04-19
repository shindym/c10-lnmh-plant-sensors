resource "aws_iam_role" "transfer-lambda-role" {
  name               = "c10-delta-transfer-terraform-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-policy.json
}

data "aws_ecr_repository" "transfer-lambda-ecr-repo" {
  name = "c10-delta-transfer"
}

data "aws_ecr_image" "transfer-lambda-image" {
  repository_name = data.aws_ecr_repository.transfer-lambda-ecr-repo.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "transfer-lambda" {
  role          = aws_iam_role.transfer-lambda-role.arn
  function_name = "c10-delta-transfer-terraform-lambda"
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.transfer-lambda-image.image_uri
  timeout       = 120
  environment {
    variables = {
      ACCESS_KEY_ID     = var.AWS_ACCESS_KEY_ID,
      DB_HOST           = var.DB_HOST,
      DB_NAME           = var.DB_NAME,
      DB_PASSWORD       = var.DB_PASSWORD,
      DB_PORT           = var.DB_PORT,
      LOCAL_FILE        = var.LOCAL_FILE,
      SCHEMA            = var.SCHEMA,
      SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY
    }
  }
}