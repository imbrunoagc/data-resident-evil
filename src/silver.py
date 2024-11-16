import os
from datetime import datetime
from typing import List

import boto3
import pandas as pd

from resources.boto3_manager import PandasBucket
from tools.transform import (
    extract_height,
    extract_number,
    extract_type_sanguine,
    extract_weight,
    extract_year,
)

print("### Acesso o Modulo Silver.py ###")

class ResidentEvil_Bronze_to_Silver:
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

    def _get_json_from_s3(self) -> List:
        s3_resident = self.__get_bucket('resident-evil')
        return s3_resident.read_json_from_s3('bronze/person_characters.json')
    
    def _transform_json_to_dataframe(self) -> pd.DataFrame:
        data_json = self._get_json_from_s3()
        df = pd.DataFrame(data_json)
        df['ano_de_nascimento'] = df['Ano de nascimento'].fillna(df['de nascimento']).apply(extract_year)
        df['tipo_sanguineo'] = df['Tipo sanguíneo'].apply(extract_type_sanguine)
        df['altura'] = df['Altura'].apply(extract_height)
        df['peso'] = df['Peso'].apply(extract_weight)
        df['altura'] = df['altura'].apply(extract_number) # extração apenas do valor numerico
        df['peso'] = df['peso'].apply(extract_number) # extração apenas do valor numerico
        df['pathimage'] = 'https://www.residentevildatabase.com/wp-content/uploads/2023/12/' + df['name'] +'.jpg'
        df['IngestionDate'] = datetime.now().strftime('%Y-%m-%d')
        df['IngestionTime'] = datetime.now().strftime('%H:%M:%S')
        df['Source'] = 'DataResidentEvil'
        df = df.drop(columns={'Ano de nascimento', 'de nascimento', 'Tipo sanguíneo', 'Altura', 'Peso'})
        return df
    
    def bronze_to_silver(self):
        s3_resident = self.__get_bucket('resident-evil')
        df = self._transform_json_to_dataframe()
        s3_resident.put_parquet(df, 'silver/person_characters.parquet')
        
        print("### Finalizou o Modulo Silver.py ###")
    

if __name__ == "__main__":
    ResidentEvil_Bronze_to_Silver().bronze_to_silver()
