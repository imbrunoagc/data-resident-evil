import os
import pandas as pd
import boto3
from src.resources.boto3_manager import PandasBucket

client = boto3.client(
                's3',
                endpoint_url='http://localhost:9000', #os.environ.get('ENDPOINT'),  # Correct API port
                aws_access_key_id=os.environ.get('ACCESS_KEY'),
                aws_secret_access_key=os.environ.get('SECRET_KEY'),
                region_name='us-east-1'
            )

def readFile(name_file_gold: str) -> pd.DataFrame:
    s3 = PandasBucket(client, 'resident-evil')
    return s3.read_parquet(f'gold/{name_file_gold}.parquet')