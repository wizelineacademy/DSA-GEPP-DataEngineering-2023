import io
import json
import logging
import os
import zipfile

import boto3
import pandas as pd
import requests

from botocore.exceptions import ClientError
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

# Setting LOG level and format, for mor info visit https://www.logicmonitor.com/blog/python-logging-levels-explained
logging.basicConfig(format='%(levelname)s : %(message)s',
                    level=logging.INFO)

DAG_ID = os.path.splitext(os.path.basename(__file__))[0]

# Values to change according your own configs
S3_BUCKET = 'my-s3-bucket-john'
FILE_NAME = "denue_inegi_09_.csv"
URL = 'https://www.inegi.org.mx/contenidos/masiva/denue/denue_09_csv.zip'

# Constant values
SECRET_NAME = "rds-mysql"
REGION_NAME = "us-east-1"
S3_KEY_ORIGINAL = f"session-14-airflow/denue/original/{FILE_NAME}"
S3_KEY_FINAL = f"session-14-airflow/denue/final/{FILE_NAME}"

# Setting the config for the Session
session = boto3.session.Session()
secrets_client = session.client(
        service_name='secretsmanager',
        region_name=REGION_NAME
    )

# Getting the secrets
secrets_list = [SECRET_NAME]
secrets = {
        x: secrets_client.get_secret_value(
            SecretId=f"airflow/connections/dev/{x}"
        )['SecretString'] for x in secrets_list
    }

def get_secret(secret, region):
    """
    Get the secret from AWS Secrets Manager
    
    :param secret (str): Name of the Secret
    :param region (str): Region in which the Secret is stored
    :param profile (str): Profile name to be executed, left in blank to take default (optional)
    
    :return: String with the Secret Value
    """    
    
    secret_name = secret

    # Create a Secrets Manager client
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = json.loads(get_secret_value_response['SecretString'])

    return secret

def upload_file_to_s3(bucket_name, s3_key, file_object, region, profile="default"):
    """
    Upload a file to an S3 bucket
    
    :param file_path (str): Local file path of the file to upload
    :param bucket_name (str): Name of the S3 bucket to upload the file to
    :param s3_key (str): S3 key (i.e. object name) to assign to the file in the bucket
    :param region (str): Region in which the Secret is stored
    :param profile (str): Profile name to be executed, left in blank to take default (optional)
    
    :return: botocore.response object. If error, returns None.
    """
    
    # Create S3 client
    s3_client = session.client(
        service_name='s3',
        region_name=region
    )
    
    try:
        # Upload file to S3 bucket from local
        # s3_client.upload_file(file_path, bucket_name, s3_key)
        
        # Upload file to S3 bucket from memory (Body)
        response = s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=file_object)
        
        logging.info(f"Successfully uploaded {s3_key} to S3 bucket {bucket_name}")
    
    except Exception as e:
        logging.info(f"Error uploading file to S3: {e}")
        raise e
    
    return response

def get_s3_object(bucket_name, object_name, region, profile="default"):
    """
    Retrieve an object from an S3 bucket
    
    :param bucket_name: string
    :param object_name: string
    
    :return: botocore.response object. If error, returns None.
    """
    # Create S3 client
    s3_client = session.client(
        service_name='s3',
        region_name=region
    )
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        logging.info(f"Successfully get {object_name} from S3 bucket {bucket_name}")
        
    except ClientError as e:
        logging.info(f"Error getting object {object_name} from bucket {bucket_name}: {e}")
        raise e
    
    return response

def download_and_upload_to_s3(bucket_name, s3_key, url):
    """
    Download the data from the external URL and upload it 
    decompressed to s3
    
    :param bucket_name (str): Bucket name
    :param s3_key (str): S3 key that includes the whole path with the file name
    :param url (str): URL of the external data
    
    :return: botocore.response object. If error, returns None.
    """  
    
    try:
        # Download file from URL
        response = requests.get(url)

        # Extract CSV file from ZIP archive
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            csv_filename = [f for f in z.namelist() if f.endswith(s3_key.split('/')[-1])][0]
            csv_file = z.read(csv_filename)

        # Uploading the data to s3
        response = upload_file_to_s3(bucket_name, s3_key, csv_file, REGION_NAME)

        return response
        
    except requests.exceptions.RequestException as e:
        logging.info(f"Failed to download data from {url}: {e}")
        raise e
        
    except zipfile.BadZipFile as e:
        logging.info(f"Failed to extract CSV file from ZIP archive: {e}")
        raise e
        
    except boto3.exceptions.Boto3Error as e:
        logging.info(f"Failed to upload {key_name} to S3 bucket {bucket_name}: {e}")
        raise e
    
def get_body_content(bucket_name, s3_key):
    """
    Gets the object.
    
    :param bucket_name (str): Bucket name
    :param s3_key (str): S3 key that includes the whole path with the file name

    :return: The object data in as a dataframe with correct column names
    """
    try:

        response = get_s3_object(bucket_name, s3_key, REGION_NAME)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        logging.info(status)
        
        # Writing the file to the local file system
        with open(f"/tmp/{FILE_NAME}",'wb') as output_file:
            output_file.write(response.get("Body").read())
        
        logging.info(f'Download file /tmp/{FILE_NAME} completed')
        
        if status == 200:
            # Get columns for df
            df = pd.read_csv(f"/tmp/{FILE_NAME}", encoding='latin-1')
            return df
        else:
            raise ClientError

    except ClientError as e:
        logging.info("Couldn't get object from bucket .")
        raise e
    except Exception as e:
        logging.info("Error when creating dataframe")
        logging.info(e)
        raise e
    
def clean_data(df_data, bucket_name, s3_key):
    # Filter by activities
    options = [461110,461111,461112,461113]
    gepp_data = df_data[df_data["codigo_act"].isin(options)]
    
    # cod_postal column should always have 5 digits
    gepp_data = gepp_data.astype({'cod_postal': 'string'})
    gepp_data["cod_postal"] = gepp_data["cod_postal"].str.replace(".0",'' , regex=False)
    gepp_data.dropna(subset=['cod_postal'], inplace=True)
    gepp_data["cod_postal"] = gepp_data["cod_postal"].apply(lambda x: x if len(x) == 5 else '0'+ x)
    
    # The entity is always Mexico City and the key is always 9
    gepp_data["is_city_valid"] = gepp_data.apply(lambda row : True if  row['cve_ent'] == 9 and row['entidad'] == "CIUDAD DE MÉXICO" else False , axis=1)    
    final_data = gepp_data[gepp_data["is_city_valid"]]
    final_data.drop(columns="is_city_valid", inplace=True)
    
    # Uploading the data to s3
    response = upload_file_to_s3(bucket_name, s3_key, final_data.to_csv(), REGION_NAME)
    
    if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
        return True
    else:
        return False
    
def extract_denue_inegi(**kwargs):
    """
    This function will extract the data from Inegi
    then will be decompressed and uploaded in csv files
    into a S3 bucket (Original)
    """

    bucket_name = kwargs['bucket_name']
    s3_key = kwargs['s3_key']
    url = kwargs['url']
    
    download_and_upload_to_s3(bucket_name, s3_key, url)

def transform_denue_inegi(**kwargs):
    """
    This function will transform the data from Inegi
    will take the data stored in S3, then download it 
    locally and perform some transformations and at the
    end the data will be stored in S3 (Final)
    """

    bucket_name = kwargs['bucket_name']
    s3_key_original = kwargs['s3_key_original']
    s3_key_final = kwargs['s3_key_final']
    
    df_denue = get_body_content(bucket_name, s3_key_original)
    clean_data(df_denue, bucket_name, s3_key_final)

default_args = {
    'owner': 'airflow',    
    'start_date': datetime(2023, 5, 9),
    'schedule_interval': '0 8 * * *',
    #'end_date': datetime(),
    #'depends_on_past': False,
    #'email': ['email@domain.com'],
    #'email_on_failure': True,
    #'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

@dag(
    dag_id=DAG_ID,
    default_args=default_args,
    catchup=False,
    tags=['dsa-gepp','demo-mwaa'],
)

def create_dag():
    begin = DummyOperator(task_id="begin")
    end = DummyOperator(task_id="end")

    extract = PythonOperator(
        task_id="extract_denue_inegi",
        python_callable=extract_denue_inegi,
        op_kwargs={
            'bucket_name': S3_BUCKET, 
            's3_key': S3_KEY_ORIGINAL, 
            'url': URL                                
        }
    )

    transform = PythonOperator(
        task_id="transform_denue_inegi",
        python_callable=transform_denue_inegi,
        op_kwargs={
            'bucket_name': S3_BUCKET, 
            's3_key_original': S3_KEY_ORIGINAL, 
            's3_key_final': S3_KEY_FINAL                              
        }
    )

    begin >> extract >> transform >> end

globals()[DAG_ID] = create_dag()