import os
import pandas as pd
from minio import Minio
from dotenv import load_dotenv
from resources.minio_manager import PandasBucket
from bronze import Bronze

load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '.env'))

print("acess: ", os.getenv('ACCESS_KEY'))
client = Minio(endpoint=os.getenv('ENDPOINT'), access_key=os.getenv('ACCESS_KEY'), secret_key=os.getenv('SECRET_KEY'), secure=False)

s3_bronze = PandasBucket(client=client, name="resident-evil")

bronze_cls = Bronze()
data = bronze_cls.get_data_json('data/raw/raw_characters.json')
data = bronze_cls.add_data_processed(data)
print(data)

s3_bronze.write_dict_to_json(data, "bronze/person_characters")