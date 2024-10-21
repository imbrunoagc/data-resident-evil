import json
from datetime import datetime
from typing import List, Dict

class Bronze():
    def get_data_json(self, path_file:str) -> List:
        try:
            with open(path_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print("Arquivo JSON não encontrado.")
        except json.JSONDecodeError:
            print("Erro ao decodificar o arquivo JSON.")

    def add_data_processed(self, data:list) -> list:
        now = datetime.now()
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    item['date_processed'] = now.isoformat()
        return data

    def write_data_raw(self, data: Dict, file_path: str) -> None:
        with open(file_path, 'w') as output_file:
            try:
                json.dump(data, output_file, indent=2)
                print(f'success in writing the file: {file_path}')
            except Exception as e:
                print(f'Error: {e}')

if __name__ == "__main__":
    bronze = Bronze()
    data = bronze.get_data_json('../data/raw/raw_characters.json')
    data = bronze.add_data_processed(data)
    bronze.write_data_raw(data, '../data/bronze/bronze_characters.json')