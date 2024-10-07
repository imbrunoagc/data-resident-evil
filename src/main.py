import json
from pydantic import ValidationError
from sqlalchemy.orm import Session
from database import database
from models import models
from schemas import schemas

models.Base.metadata.create_all(bind=database.engine) # create tbales

def create_person(person: models.CharactersPerson, db: Session = database.get_db):
    db_basic = models.CharactersPerson(**person.dict())
    db.add(db_basic)
    db.commit()
    db.refresh(db_basic)
    #return db_basic


def executor_bronze():
    try:
        with open('data/raw/basic_information_characters.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # por item da lista, validar o schema 
        for character_data in data:
            try:
                character = schemas.CharactersPerson(**character_data)
                create_person(character)
                #print(character)
            except ValidationError as e:
                print(f"Erro de validação para {character_data['name']}: {e}")
        print("\nSucesso na leitura utilizando o schema pydantic.")

    except FileNotFoundError:
        print("Arquivo JSON não encontrado.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")

if __name__ == "__main__":
    executor_bronze()