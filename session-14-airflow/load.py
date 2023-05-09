import json
import requests
import boto3
from botocore.exceptions import ClientError
import zipfile



def lambda_handler(event, context):
    
    bucket = 'gepp-wizeline-bronze'
    
    print('Downloading started')
    url = 'https://www.inegi.org.mx/contenidos/masiva/denue/denue_09_csv.zip'
    # TODO implement
    denue = requests.get(url)
   # Split URL to get the file name
    filename = url.split('/')[-1]
     
    # Writing the file to the local file system
    with open("/tmp/"+filename,'wb') as output_file:
        output_file.write(denue.content)
    print('Downloading Completed')
    
    with zipfile.ZipFile("/tmp/" + filename, 'r') as zip_ref:
        zip_ref.extractall('/tmp/')
    
    print('S3 Upload Start')
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file("/tmp/conjunto_de_datos/denue_inegi_09_.csv", bucket, 'denue/denue_inegi_09_.csv')
    print('S3 Upload Completed')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda successfuly executed!')
    }
