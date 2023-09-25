import boto3
from pprint import pprint
import pathlib
import os
from flask import Flask
from flask import request

# export FLASK_RUN_PORT=8888
# export FLASK_RUN_HOST=0.0.0.0
# flask --app upload-to-s3 run

# export S3_ENDPOINT_LINK="s3.us-east-2.amazonaws.com"
# export S3_SECRET_PATH="/var/run/secrets/s3/"
# access_key_id & access_key_secret are in /var/run/secrets/s3/access_key_id & /var/run/secrets/s3/access_key_secret

s3SecretPath = os.environ.get("S3_SECRET_PATH", "/var/run/secrets/s3/")
s3EndpointLink = os.environ.get("S3_ENDPOINT_LINK", "s3.us-east-2.amazonaws.com")
verifySSL = os.environ.get("S3_VERIFY_SSL", "True")

access_key_id_path = open(s3SecretPath + 'access_key_id', "r")
access_key_secret_path = open(s3SecretPath + 'access_key_secret', "r")
access_key_id = access_key_id_path.read().strip()
access_key_secret = access_key_secret_path.read().strip()

s3 = boto3.client(service_name='s3',
                  endpoint_url="https://" + s3EndpointLink,
                  aws_access_key_id=access_key_id,
                  aws_secret_access_key=access_key_secret,
                  verify=verifySSL)

app = Flask(__name__)

def upload_file_using_client(bucket_name, object_name, file_name):
    """
    Uploads file to S3 bucket using S3 client object
    :return: None
    """
    
    # Check to see if the file exists on the local file system
    if os.path.isfile(file_name):
        response = s3.upload_file(file_name, bucket_name, object_name)
        if response is None:
            return "success"
        else:
            return "Exception: " + response
    else:
        return "ErrNotExist"

@app.route("/", methods = ['GET'])
def index():
    if request.method == 'GET':
        return "ok"

@app.route("/healthz", methods = ['GET'])
def healthz():
    if request.method == 'GET':
        return "ok"

@app.route("/upload", methods = ['POST'])
def upload():
    if request.method == 'POST':
        bucket = request.form.get('bucket')
        filename = request.form.get('filename')
        filepath = request.form.get('filepath')

        rc = upload_file_using_client(bucket, filename, filepath)
        if rc == "success":
            rData = {'status': 'success', 'message': 'File uploaded successfully'}
        else:
            rData = {'status': 'failed', 'message': rc}

        return rData
