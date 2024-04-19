data "aws_iam_policy_document" "pipeline-schedule-permissions-policy" {

  statement {
    effect = "Allow"

    resources = [
      aws_lambda_function.pipeline-lambda.arn,
      "${aws_lambda_function.pipeline-lambda.arn}:*"
    ]

    actions = ["lambda:InvokeFunction"]
  }
}

resource "aws_iam_role" "pipeline-schedule-role" {
  name               = "c10-delta-schedule-role-pipeline-terraform"
  assume_role_policy = data.aws_iam_policy_document.schedule-trust-policy.json

  inline_policy {
    name   = "c10-delta-inline-lambda-execution-policy-pipeline"
    policy = data.aws_iam_policy_document.pipeline-schedule-permissions-policy.json
  }
}

resource "aws_scheduler_schedule" "pipeline-schedule" {
  name                = "c10-delta-pipeline-schedule-terraform"
  group_name          = "default"
  schedule_expression = "cron(*/1 * * * ? *)"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.pipeline-lambda.arn
    role_arn = aws_iam_role.pipeline-schedule-role.arn
  }
}