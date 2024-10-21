import json
from typing import List
import pandas as pd

class Silver:
    def __init__(self, path_file_bronze: str, path_file_silver: str) -> None:
        self.path_file_bronze = path_file_bronze
        self.path_file_silver = path_file_silver
    
    def get_data_json(self) -> List:
        try:
            with open(self.path_file_bronze, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print("Arquivo JSON não encontrado.")
        except json.JSONDecodeError:
            print("Erro ao decodificar o arquivo JSON.")

if __name__ == "__main__":        
    silver = Silver('../data/bronze/bronze_characters.json', '../data/silver/bronze_characters.parquet')
    data = silver.get_data_json()

    df = pd.DataFrame(data)
    df['ano_nascimento'] = df['Ano de nascimento'].fillna(df['de nascimento'])
    df['ano_nascimento'].unique()
    df['Ano de nascimento'].str[:4]
