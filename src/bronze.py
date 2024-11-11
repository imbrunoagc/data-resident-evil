import os
import boto3
from dotenv import load_dotenv
from scrapy.collect import collect
from scrapy.paramns import COOKIES, HEADERS
from resources.boto3_manager import PandasBucket

load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '.env'))

print("Acessou o modulo Bronze.py")

class ResidentEvil_to_BronzeMinio:
    def __init__(self) -> None:
        self.client = boto3.client(
                's3',
                endpoint_url='http://localhost:9000',  # Correct API port
                aws_access_key_id=os.getenv('ACCESS_KEY'),
                aws_secret_access_key=os.getenv('SECRET_KEY'),
                region_name='us-east-1'
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

    print("Finlizou o Modulo Bronze.py")