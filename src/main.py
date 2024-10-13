import json

def executor_bronze():
    try:
        with open('data/raw/basic_information_characters.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        print("Arquivo JSON não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")

if __name__ == "__main__":
    executor_bronze()