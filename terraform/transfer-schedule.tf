data "aws_iam_policy_document" "transfer-schedule-permissions-policy" {

  statement {
    effect = "Allow"

    resources = [
      aws_lambda_function.transfer-lambda.arn,
      "${aws_lambda_function.transfer-lambda.arn}:*"
    ]

    actions = ["lambda:InvokeFunction"]
  }
}

resource "aws_iam_role" "transfer-schedule-role" {
  name               = "c10-delta-schedule-role-transfer"
  assume_role_policy = data.aws_iam_policy_document.schedule-trust-policy.json

  inline_policy {
    name   = "c10-delta-inline-lambda-execution-policy-transfer"
    policy = data.aws_iam_policy_document.transfer-schedule-permissions-policy.json
  }
}

resource "aws_scheduler_schedule" "transfer-schedule" {
  name                = "c10-delta-transfer-schedule"
  group_name          = "default"
  schedule_expression = "cron(00 18 * * ? *)"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.transfer-lambda.arn
    role_arn = aws_iam_role.transfer-schedule-role.arn
  }
}