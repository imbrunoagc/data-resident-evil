from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CharactersPerson(Base):
    __tablename__ = 'bronze.characters_person'

    id = Column(Integer, primary_key=True, index=True)
    ano_de_nascimento = Column(String, nullable=True)
    tipo_sanguineo = Column(String, nullable=True)
    altura = Column(String, nullable=True)
    peso = Column(String, nullable=True)
    aparicoes = Column(String, nullable=True)
    link = Column(String, nullable=True)
    name = Column(String, nullable=True)