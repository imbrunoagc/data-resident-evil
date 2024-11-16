import os
import pandas as pd
from typing import List
from datetime import datetime
import boto3
from resources.boto3_manager import PandasBucket
from tools.rules_gold import ( 
                            explode_dataframe, top_10_most_popular_characters, 
                            blood_type_distribution, average_height_and_weight_by_blood_type )

class ResidentEvil_Silver_to_Gold:
    def __init__(self) -> None:
        self.client = boto3.client(
                's3',
                endpoint_url='http://localhost:9000', #os.environ.get('ENDPOINT'),  # Correct API port
                aws_access_key_id=os.environ.get('ACCESS_KEY'),
                aws_secret_access_key=os.environ.get('SECRET_KEY'),
                region_name='us-east-1'
            )
    
    def __get_bucket(self, name_bucket: str):
        return PandasBucket(client=self.client, name=name_bucket)

    def _get_parquet_s3(self) -> List:
        s3_resident = self.__get_bucket('resident-evil')
        return s3_resident.read_parquet(name='silver/person_characters.parquet') # hardcoded
    
    def build_and_loadS3(self, df: pd.DataFrame, name_file: str) -> None:
        s3_resident = self.__get_bucket('resident-evil')
        s3_resident.put_parquet(df, f'gold/{name_file}.parquet')
    
if __name__ == "__main__":
    cls_gold = ResidentEvil_Silver_to_Gold()
    data = cls_gold._get_parquet_s3()
    
    df_exploded = explode_dataframe(data, 'aparicoes') #exploded data
    
    cls_gold.build_and_loadS3(df_exploded, 'characters_exploded')
    cls_gold.build_and_loadS3(top_10_most_popular_characters(df_exploded), 'top_10_most_popular_characters')
    cls_gold.build_and_loadS3(blood_type_distribution(data), 'blood_type_distribution')
    cls_gold.build_and_loadS3(average_height_and_weight_by_blood_type(data), 'average_by_blood_type')