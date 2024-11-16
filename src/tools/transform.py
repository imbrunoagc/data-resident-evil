import re
from datetime import datetime

def extract_year(value) -> str:
    if isinstance(value, str):
        year = value.strip()[:4]
        if year.isdigit():
            year = int(year)
            current_year = datetime.now().year
            if 1900 <= year <= current_year:
                return str(year)
    return 'Desconhecido'

def extract_type_sanguine(value: str) -> str:
    if isinstance(value, str):
        value = value.strip().lower()
        map = {
            '\xa0desconhecido.': 'Desconhecido',
            'desconhecido.': 'Desconhecido',
            'desconhecido': 'Desconhecido',
            'desconhecido': 'Desconhecido'
        }
        return map.get(value, value.upper())
    return 'Desconhecido'

def extract_height(value) -> str:
    if isinstance(value, str):  # Verifica se o valor é uma string
        match = re.search(r'\b\d+,\d+(?:m|cm)\b', value) # Busca o primeiro padrão que corresponde a altura (ex: 1,75m ou 1,75cm)

        if match:
            return match.group(0)
    return "Desconhecido"

def extract_weight(value) -> str:
    if isinstance(value, str):     # Verifica se o valor é uma string
        match = re.search(r'\b\d+(?:,\d+)?kg\b', value)  # Busca o primeiro padrão que corresponde ao peso (ex: 84,5kg ou 84kg)
        if match:
            return match.group(0)
    return "Desconhecido"


def extract_number(value):
    match = re.match(r"([0-9,\.]+)", str(value)) # Expressão regular para capturar o número (incluindo vírgula ou ponto como separador decimal)
    if match:
        return float(match.group(1).replace(',', '.'))  # Converte para float, substituindo vírgula por ponto
    return None  # Retorna None se não houver número válido