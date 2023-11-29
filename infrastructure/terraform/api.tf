resource "aws_api_gateway_rest_api" "default" {
  name = var.name
}

resource "aws_api_gateway_resource" "slack_resource" {
  rest_api_id = aws_api_gateway_rest_api.default.id
  parent_id   = aws_api_gateway_rest_api.default.root_resource_id
  path_part   = "slack"
}

resource "aws_api_gateway_resource" "events_resource" {
  rest_api_id = aws_api_gateway_rest_api.default.id
  parent_id   = aws_api_gateway_resource.slack_resource.id
  path_part   = "events"
}

resource "aws_api_gateway_method" "default" {
  authorization = "NONE"
  http_method   = "POST"
  resource_id   = aws_api_gateway_resource.events_resource.id
  rest_api_id   = aws_api_gateway_rest_api.default.id
}

resource "aws_api_gateway_integration" "default" {
  rest_api_id = aws_api_gateway_rest_api.default.id
  resource_id = aws_api_gateway_method.default.resource_id
  http_method = aws_api_gateway_method.default.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.default.invoke_arn
}

resource "aws_api_gateway_deployment" "default" {
  depends_on  = [aws_api_gateway_method.method]
  rest_api_id = aws_api_gateway_rest_api.default.id
  stage_name  = var.environment
}
