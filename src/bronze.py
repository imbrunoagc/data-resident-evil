import os
from minio import Minio
from dotenv import load_dotenv
from scrapy.collect import collect
from scrapy.paramns import COOKIES, HEADERS
from resources.minio_manager import PandasBucket

load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '.env'))


class ResidentEvil_to_BronzeMinio:
    def __init__(self) -> None:
        self.client = Minio(
            endpoint=os.getenv('ENDPOINT'),
            access_key=os.getenv('ACCESS_KEY'),
            secret_key=os.getenv('SECRET_KEY'),
            secure=False
            )
        self.cookies = COOKIES
        self.headers = HEADERS
    
    def run_bronze(self, name_bucket: str, name_file: str):
        data_resident_evil = collect(self.cookies, self.headers).run_collect(if_local=False)
        s3_bronze = PandasBucket(client=self.client, name=name_bucket)
        try:
            s3_bronze.write_dict_to_json(data_resident_evil, name_file)
            print(f'success in writing the file: {name_bucket}/{name_file}')
        except Exception as e:
            print(f"Error: {e}")
                  
if __name__ == "__main__":
    ResidentEvil_to_BronzeMinio().run_bronze('resident-evil', 'bronze/person_characters.json')