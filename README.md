# Projeto: Data Resident Evil

## Coleta de Dados e Data Lake com MinIO
Este projeto de arquitetura open source tem como foco a raspagem de dados de personagens do universo ``Resident Evil``, com armazenamento em um ``data lake`` e exibição em um dashboard interativo. A construção visa boas práticas e clareza em todos os aspectos, da arquitetura à escrita do código.

### Objetivos:
* Implementar um data lake seguindo a arquitetura ``medallion``.
* Utilizar ``BeautifulSoup`` para a raspagem dos dados.
* Armazenar os dados na camada Bronze em formato JSON com Python.
* Realizar transformações nas camadas Silver e Gold com ``pandas``.
* Escrever *testes unitários* utilizando ``pytest``.
* Aplicar o ``ruff`` para garantir a *formatação* do código Python.
* Criar um dashboard com ``Streamlit`` para visualização gráfica dos dados da camada Gold.
* Subir todos os serviços via ``Docker``.

A arquitetura proposta é a seguinte:
<table>
    <td>
    <img src="assets/architecture-version_1.0.png"
></img></td></tr>
</table>

## Estrutura do Projeto
* `.git` - Controle de versão.
* `.pytest` - Configurações para testes unitários.
* `.ruff_cache` - Cache do Ruff para linting.
* `.venv` - Ambiente virtual com dependências do projeto.
* `.gitignore` - Arquivo de exclusões do Git.
* `.python-version` - Versão do python utilizada no projeto.
* `requirements.txt` - Dependências do projeto.
* `pyproject.toml` - Configurações e dependências do projeto com Poetry. 
* `README.md` - Documentação principal do projeto.
* `assets/` - Imagens e arquivos de mídia utilizados na documentação.
* `docs/` - Documentação suplementar.
* `notebook` - Analises pontuais em notebook
* `src/resources/` - Arquivo de conexão com o MinIO e demais funcionalidades de coleta e inserção.
* `src/scrapy/` - Arquivo principal com a respagem de dados do projeto.
* `src/` - Arquivo endereçados como Bronze, Silver e Gold, que é o core do projeto.
* `tests/` - Arquivo que propõe teste unitários em classes e métodos.


## Estrutura de Pastas

```bash
|
|── .gitignore
|── .python-version
|── requirements.txt
|── poetry.lock
|── pyproject.toml
|── README.md
|── src/
|   |── resources/
|   |   |── __init__.py
|   |   └── minio_manager.py
|   |── scrapy/
|   |   |── __init__.py
|   |   |── collect.py
|   |   └── paramns.py
|   |── __init__.py
|   |── bronze.py
|   |── silver.py
|   └── gold.py
|
└── tests/
        |── test_1.py
        └── test_2.py
```

## Setup do Projeto


## Como executar o ruff?


## Como executar o pytest?


## Setup de execução do projeto em Docker