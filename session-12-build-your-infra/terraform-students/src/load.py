import json
import requests
import boto3
from botocore.exceptions import ClientError
import zipfile
from datetime import datetime


# GEPP - HOMEWORK - How can we leverage event and context?
def lambda_handler(event, context):
    # GEPP - PRINT/LOG - type and dir of event and context

    # GEPP - IMPORTANT - Change to your bucket name
    bucket = 'deb-s12-bronze-smontiel'
    
    print('Downloading started')
    url = 'https://www.inegi.org.mx/contenidos/masiva/denue/denue_09_csv.zip'
    
    # GEPP - QUESTION - What is try/except good for? Thoughts first, investigate later.
    # GEPP - PRINT/LOG - Add logging statement after the exception
    try:
        denue = requests.get(url)
    except Exception as err:
        print('ERROR - REST call error obtained')
        print(err)

    print('Finished REST call')

    # GEPP - PRINT/LOG - type(denue) and dir(denue)

    # Split URL to get the file name
    filename = url.split('/')[-1]

    # GEPP - PRINT/LOG - url.split('/')
     
    # Writing the file to the local file system
    with open("/tmp/"+filename,'wb') as output_file:
        output_file.write(denue.content)
    print('Downloading Completed')
    
    with zipfile.ZipFile("/tmp/" + filename, 'r') as zip_ref:
        zip_ref.extractall('/tmp/')
    
    # GEPP - QUESTION - How to measure time?
    print('S3 Upload Start')
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file("/tmp/conjunto_de_datos/denue_inegi_09_.csv", bucket, 'denue/denue_inegi_09_.csv')
    print('S3 Upload Completed')
    
    return {
        'statusCode': 200,
        # GEPP - HOMEWORK - Customize this message with the information
        #                   that would be useful to you once the function finishes
        'body': json.dumps('Lambda successfuly executed!')
    }
