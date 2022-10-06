module "lambda_for_dem" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "4.0.2"

  function_name = "demCall"
  description   = "dem call to to feed cloudformation"
  handler       = "dem.lambda_handler"
  runtime       = "python3.9"
  source_path   = "${path.module}/lambda"
  
  # I am assuming no special role is needed, but is unlikely : )
  create_role = true
  #liklye some work need to be done to reach the connectivity of from Cloudformation
  # attach_network_policy = true

  layers = [aws_lambda_layer_version.dem_layer.arn]
  # create_package         = false
  # local_existing_package = "${path.module}/layer/functions.zip"

}


resource "aws_lambda_layer_version" "dem_layer" {
  # this zip is generated from a virtualenv as explained here: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
  filename   = "${path.module}/layer/functions.zip"
  layer_name = "dem_terraform_layer"

  compatible_runtimes = ["python3.9"]
}

