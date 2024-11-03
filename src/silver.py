import os
import pandas as pd
from typing import List
from dotenv import load_dotenv
from minio import Minio
from resources.minio_manager import PandasBucket

load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '.env'))

class ResidentEvil_Bronze_to_Silver:
    def __init__(self) -> None:
        self.client = Minio(
            endpoint=os.getenv('ENDPOINT'),
            access_key=os.getenv('ACCESS_KEY'),
            secret_key=os.getenv('SECRET_KEY'),
            secure=False
            )
        #self.path_file_bronze = path_file_bronze
        #self.path_file_silver = path_file_silver
    
    def __get_bucket(self, name_bucket: str):
        return PandasBucket(client=self.client, name=name_bucket)

    def _get_json_from_minio(self) -> List:
        s3_resident = self.__get_bucket('resident-evil')
        return s3_resident.read_json_from_minio('bronze/person_characters')
    
    def _transform_json_to_dataframe(self) -> pd.DataFrame:
        data_json = self._get_json_from_minio()
        df = pd.DataFrame(data_json)
        df['ano_nascimento'] = df['Ano de nascimento'].fillna(df['de nascimento'])
        df['ano_nascimento'].unique()
        df['Ano de nascimento'].str[:4]
        return df
    
    def bronze_to_silver(self):
        s3_resident = self.__get_bucket('resident-evil')
        df = self._transform_json_to_dataframe()
        s3_resident.put_parquet(df, 'silver/person_characters')
    

if __name__ == "__main__":        
    #ResidentEvil_Bronze_to_Silver()._transform_json_to_dataframe()
    ResidentEvil_Bronze_to_Silver().bronze_to_silver()
