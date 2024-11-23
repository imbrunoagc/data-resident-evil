import os

import boto3

from resources.boto3_manager import PandasBucket
from scrapy.collect import collect
from scrapy.paramns import COOKIES, HEADERS


class ResidentEvil_to_BronzeMinio:
    def __init__(self) -> None:
        self.client = boto3.client(
            's3',
            endpoint_url=os.environ.get('ENDPOINT'),
            aws_access_key_id=os.environ.get('ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('SECRET_KEY'),
            region_name='us-east-1',
        )
        self.cookies = COOKIES
        self.headers = HEADERS

    def run_bronze(self, name_bucket: str, name_file: str):
        data_resident_evil = collect(self.cookies, self.headers).run_collect(
            if_local=False
        )
        s3_bronze = PandasBucket(client=self.client, name=name_bucket)
        try:
            s3_bronze.write_dict_to_json(data_resident_evil, name_file)
            print(f'success in writing the file: {name_bucket}/{name_file}')
        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    ResidentEvil_to_BronzeMinio().run_bronze(
        'resident-evil', 'bronze/person_characters.json'
    )

    print('### 1. Finished the Bronze.py Module')
