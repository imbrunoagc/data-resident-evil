# tests/test_main.py
import pytest
from unittest.mock import patch, mock_open
from resident_evil_request.collect import write_data_raw
from resident_evil_request.paramns import COOKIES, HEADERS

FAKE_DADOS = {"nome": "Exemplo", "valor": 123}

def test_write_data_raw():
    """Teste para a função write_data_raw usando mock de open."""
    with patch("builtins.open", mock_open()) as mock_file:
        # Chame a função sem passar o caminho (já definido no main)
        write_data_raw(FAKE_DADOS)

        # Verifica se o arquivo foi aberto com o FILE_PATH definido no código
        mock_file.assert_called_once_with('w')
        # Verifica se os dados foram gravados corretamente
        mock_file().write.assert_called_once(FAKE_DADOS)