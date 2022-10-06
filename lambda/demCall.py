import json
from python_terraform import *
import requests

LAMBDA_FOLDER = '/tmp/'

def download_tfstate(bucket_name, file_name):
    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucket_name).download_file(file_name, LAMBDA_FOLDER + file_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def terraform_output(alb_output):
  tf = Terraform(working_dir=LAMBDA_FOLDER)
  # this should return a json like...  
  #{'alb_url_example': {'sensitive': False, 'type': 'string', 'value': 'http://lb-5YI-project-alpha-dev-2144336064.us-east-1.alb.amazonaws.com/'}}
  tfoutput = tf.output()
  try:
    return tfoutput[alb_url_example]['value']
  except Exception as error:
    print('Error: ' + repr(error))

def lambda_handler(event, context):
    """
    event input like:
    {
      "tfname": "terraform.tfstate", # tfstate file name
      "bucket_name": "yourbucket", # buket where it is stored
      "output": "alb_url_example" # output requested
    }
    """
    print("We started the handler")  
    download_tfstate(event['bucket_name'], event['tfname'])
    result = {}
    result['output'] = event.get('output', 'alb_url_example')

    terraform_output(output)
    return {
        'statusCode': 200,
        'body': json.dumps(result)

    }
