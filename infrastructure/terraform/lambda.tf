resource "aws_lambda_function" "default" {
  function_name = var.name
  runtime       = "python3.9"
  timeout       = 3
  handler       = "main.lambda_handler"
  memory_size   = 128
  role          = aws_iam_role.default.arn
  architectures = ["x86_64"]

  s3_bucket = var.storage_bucket
  s3_key    = "${var.name}/${var.build_number}.zip"

  environment {
    variables = {
      SLACK_SIGNING_SECRET = var.signing_secret
      SLACK_BOT_TOKEN      = var.slack_bot_token
    }
  }
}

resource "aws_iam_role" "default" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_lambda_permission" "default" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.default.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = aws_api_gateway_deployment.default.execution_arn
}
