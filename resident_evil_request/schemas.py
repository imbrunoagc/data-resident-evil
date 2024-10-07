from pydantic import BaseModel, ValidationError
from typing import List, Optional

# Schema para validação
class CharactersPerson(BaseModel):
    ano_de_nascimento: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    altura: Optional[str] = None
    peso: Optional[str] = None
    aparicoes: Optional[List[str]] = None
    link: Optional[str] = None
    name: Optional[str] = None