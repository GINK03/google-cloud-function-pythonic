import requests
import os
SECRET = os.environ['SECRET']
def lambda_handler(event, context):
    res = requests.get('https://us-central1-wild-yukikaze.cloudfunctions.net/pycall_aws_observe?secret='  + SECRET)
    return res.status_code
