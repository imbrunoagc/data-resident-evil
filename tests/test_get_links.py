# tests/test_main.py
import os
import sys
from unittest.mock import patch

dir_current = os.path.abspath(os.path.dirname(__file__))
print(dir_current)

sys.path.append(os.path.join(dir_current))
from src.scrapy.collect import get_links

# Dados simulados para os testes
FAKE_URL = 'https://api.exemplo.com/links'
FAKE_LINKS = ['https://link1.com', 'https://link2.com']


def test_get_links():
    """Teste para a função get_links com mock da URL."""
    with patch('main.requests.get') as mock_get:
        # Simulando a resposta da URL fixa
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'links': FAKE_LINKS}

        resultado = get_links()
        assert resultado == FAKE_LINKS
