from pydantic import ValidationError
import json
from src.schemas.schemas import CharactersPerson

if __name__ == '__main__':
    # Carregando o arquivo JSON
    try:
        with open('data/raw/basic_information_characters.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # por item da lista, validar o schema 
        for character_data in data:
            try:
                character = CharactersPerson(**character_data)
                #print(character)
            except ValidationError as e:
                print(f"Erro de validação para {character_data['name']}: {e}")
        print("\nSucesso na leitura utilizando o schema pydantic.")

    except FileNotFoundError:
        print("Arquivo JSON não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")
