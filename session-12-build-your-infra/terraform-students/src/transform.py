import json
import boto3
from botocore.exceptions import ClientError
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# GEPP - IMPORTANT - Change to your bucket names
BRONZE_BUCKET = 'deb-s12-bronze-smontiel'
SILVER_BUCKET = 'deb-s12-silver-smontiel'

# GEPP - QUESTION - Why is this useful?
s3 = boto3.resource('s3')
bucket = s3.Bucket(BRONZE_BUCKET)
silver_bucket= s3.Bucket(SILVER_BUCKET)
s3_client = boto3.client('s3')

# GEPP - HOMEWORK - Explore adding execution time logs        
def get_body_content():
    """
    Gets the object.

    :return: The object data in as a dataframe with correct column names
    """
    try:

        # GEPP - QUESTION - Should all messages follow a convention?
        print("inicio de get_body_content")
        # GEPP - HOMEWORK - Explore objects with type and dir
        response = s3_client.get_object(Bucket=BRONZE_BUCKET, Key="denue/denue_inegi_09_.csv")
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        print(status)
        
        # Writing the file to the local file system
        with open("/tmp/denue_inegi_09_.csv",'wb') as output_file:
            output_file.write(response.get("Body").read())
        print('Downloading Completed')

        # GEPP - QUESTION - Why 200?
        if status == 200:
            print(
                f"Successful S3 get_object response. Status - {status}")
            # Get columns for df
            
            df = pd.read_csv("/tmp/denue_inegi_09_.csv",
                              #nrows=9000,
                              encoding='latin-1'
                             )
            print(df)
            return df
        else:
            logger.info(
                f"Unsuccessful S3 get_object response. Status - {status}")
            raise ClientError

    except ClientError:
        logger.info(
            "Couldn't get object from bucket .")
        raise
    except Exception as e:
        logger.info("Error when creating dataframe")
        logger.info(e)
        raise

def clean_data( data):
    # Remover duplicados
    #data.drop_duplicates(inplace=True)
    
    # GEPP - QUESTION - What if we need the same code for different options?
    # Filtrar por actividades
    options = [461110,461111,461112,461113]
    gepp_data = data[data["codigo_act"].isin(options)]
    
    # GEPP - QUESTION - Which pandas commands take longer? how can we tell through prints?
    # cod_postal debería tener siempre 5 digitos
    gepp_data = gepp_data.astype({'cod_postal': 'string'})
    gepp_data["cod_postal"] = gepp_data["cod_postal"].str.replace(".0",'' , regex=False)
    gepp_data.dropna(subset=['cod_postal'], inplace=True)
    gepp_data["cod_postal"] = gepp_data["cod_postal"].apply(lambda x: x if len(x) == 5 else '0'+ x)
    
    # La entidad siempre es  Ciudad de México y la clave siempre es 9
    gepp_data["is_city_valid"] = gepp_data.apply(lambda row : True if  row['cve_ent'] == 9 and row['entidad'] == "CIUDAD DE MÉXICO" else False , axis=1)    
    final_data = gepp_data[gepp_data["is_city_valid"]]
    final_data.drop(columns="is_city_valid", inplace=True)
    print(final_data)
    
    print("Let's put the object in S3")
    response = s3_client.put_object(
                    Bucket=SILVER_BUCKET, Key="denue/denue_09_csv_silver.csv", Body=final_data.to_csv()
                )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        logger.info(f"Successful S3 put_object response. Status - {status}")
    else:
        logger.info(f"Unsuccessful S3 put_object response. Status - {status}")

def lambda_handler(event, context):
    
    file_data = get_body_content()
    clean_data(file_data)
    return {
        # GEPP - HOMEWORK - Customize this message with the information
        #                   that would be useful to you once the function finishes
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
