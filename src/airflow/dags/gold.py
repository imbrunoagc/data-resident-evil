import os
from typing import List

import boto3
import pandas as pd

from resources.boto3_manager import PandasBucket
from tools.rules_gold import (
    average_height_and_weight_by_blood_type,
    blood_type_distribution,
    explode_dataframe,
    top_10_characters_with_most_appearances,
    top_10_most_popular_appearances,
)

dir_current = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(dir_current, '..')


class ResidentEvil_Silver_to_Gold:
    def __init__(self) -> None:
        self.client = boto3.client(
            's3',
            endpoint_url=os.environ.get('MINIO_ENDPOINT'),
            aws_access_key_id=os.environ.get('MINIO_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('MINIO_SECRET_KEY'),
            region_name='us-east-1',
        )


    def __get_bucket(self, name_bucket: str):
        return PandasBucket(client=self.client, name=name_bucket)

    def _get_parquet_s3(self) -> List:
        s3_resident = self.__get_bucket('resident-evil')
        return s3_resident.read_parquet(
            name='silver/person_characters.parquet'
        )  # hardcoded

    def build_and_loadS3(self, df: pd.DataFrame, name_file: str) -> None:
        s3_resident = self.__get_bucket('resident-evil')
        s3_resident.put_parquet(df, f'gold/{name_file}.parquet')

    def generate_tables_gold(self):
        data = self._get_parquet_s3()

        # Exploded data
        df_exploded = explode_dataframe(data, 'aparicoes')
        df_top_10 = top_10_characters_with_most_appearances(df_exploded)
        df_top_10_appearances = top_10_most_popular_appearances(df_exploded)
        df_blood_type_distribution = blood_type_distribution(data)
        df_average_by_blood_type = average_height_and_weight_by_blood_type(data)
        
        self.build_and_loadS3(df_exploded, 'characters_exploded')
        self.build_and_loadS3(
            df_top_10_appearances, 'top_10_most_popular_appearances'
        )
        self.build_and_loadS3(
            df_top_10, 'top_10_characters_with_most_appearances'
        )
        self.build_and_loadS3(
            df_blood_type_distribution, 'blood_type_distribution'
        )
        self.build_and_loadS3(
            df_average_by_blood_type, 'average_by_blood_type'
        )

if __name__ == '__main__':
    cls_gold = ResidentEvil_Silver_to_Gold()
    data = cls_gold._get_parquet_s3()

    # Exploded data
    df_exploded = explode_dataframe(data, 'aparicoes')
    df_top_10 = top_10_characters_with_most_appearances(df_exploded)
    df_top_10_appearances = top_10_most_popular_appearances(df_exploded)
    df_blood_type_distribution = blood_type_distribution(data)
    df_average_by_blood_type = average_height_and_weight_by_blood_type(data)

    # Save Local
    df_exploded.to_parquet(
        os.path.join(path, 'data', 'characters_exploded.parquet'),
        engine='pyarrow',
    )
    df_top_10.to_parquet(
        os.path.join(
            path, 'data', 'top_10_characters_with_most_appearances.parquet'
        ),
        engine='pyarrow',
    )
    df_top_10_appearances.to_parquet(
        os.path.join(path, 'data', 'top_10_appearances.parquet'),
        engine='pyarrow',
    )
    df_blood_type_distribution.to_parquet(
        os.path.join(path, 'data', 'blood_type_distribution.parquet'),
        engine='pyarrow',
    )
    df_average_by_blood_type.to_parquet(
        os.path.join(path, 'data', 'average_by_blood_type.parquet'),
        engine='pyarrow',
    )

    # Load Layer Gold in S3
    cls_gold.build_and_loadS3(df_exploded, 'characters_exploded')
    cls_gold.build_and_loadS3(
        df_top_10_appearances, 'top_10_most_popular_appearances'
    )
    cls_gold.build_and_loadS3(
        df_top_10, 'top_10_characters_with_most_appearances'
    )
    cls_gold.build_and_loadS3(
        df_blood_type_distribution, 'blood_type_distribution'
    )
    cls_gold.build_and_loadS3(
        df_average_by_blood_type, 'average_by_blood_type'
    )

    print('### 3. Finished the Gold.py Module')
