resource "aws_iam_role" "pipeline-lambda-role" {
  name               = "c10-delta-pipeline-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-policy.json
}

data "aws_ecr_repository" "pipeline-lambda-ecr-repo" {
  name = "c10-delta-pipeline"
}

data "aws_ecr_image" "pipeline-lambda-image" {
  repository_name = data.aws_ecr_repository.pipeline-lambda-ecr-repo.name
  image_tag       = "latest"
}

resource "aws_lambda_function" "pipeline-lambda" {
  role          = aws_iam_role.pipeline-lambda-role.arn
  function_name = "c10-delta-pipeline-lambda"
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.pipeline-lambda-image.image_uri
  memory_size   = 150
  timeout       = 300
  environment {
    variables = {
      ACCESS_KEY_ID     = var.AWS_ACCESS_KEY_ID,
      SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY,
      DB_HOST           = var.DB_HOST,
      DB_NAME           = var.DB_NAME,
      DB_USER           = var.DB_USER,
      DB_PASSWORD       = var.DB_PASSWORD,
      DB_PORT           = var.DB_PORT,
      SCHEMA            = var.SCHEMA,
      storage_folder    = var.storage_folder
    }
  }
}