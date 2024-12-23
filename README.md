# 🎯 Projeto: Data Resident Evil

## Coleta de Dados e Data Lake com MinIO
Este projeto de arquitetura open source tem como foco a raspagem de dados de personagens do universo ``Resident Evil``, com armazenamento em um ``data lake`` e exibição em um dashboard interativo. A construção visa boas práticas e clareza em todos os aspectos, da arquitetura à escrita do código.

### Objetivos:
* Implementar um data lake seguindo a arquitetura ``medallion``.
* Utilizar ``BeautifulSoup`` para a raspagem dos dados.
* Armazenar os dados na camada Bronze em formato JSON com Python.
* Realizar transformações nas camadas Silver e Gold com ``pandas``.
* Utilizar o airflow para orquestrar as ``camadas``.
* Escrever *testes unitários* utilizando ``pytest`` - Local.
* Aplicar o ``ruff`` para garantir a *formatação* do código Python - Local.
* Criar um dashboard com ``Streamlit`` para visualização gráfica dos dados da camada Gold.
* Subir todos os serviços via ``Docker``.

A arquitetura proposta é a seguinte:
<table>
    <td>
    <img src="assets/architecture-version_2.0.png"
></img></td></tr>
</table>

**Principais ferramentas utilizadas no projeto:**  
- **Apache Airflow**: Responsável por orquestrar pipelines de dados, automatizando tarefas e seus agendamentos;  
- **MinIO**: Armazenamento de objetos gratuito usado para guardar e organizar os dados;  
- **Pandas**: Biblioteca Python usada para processar, transformar e analisar os dados;  
- **Docker**: Plataforma para criar e gerenciar containers, garantindo que os serviços rodem de forma consistente;  
- **Streamlit**: Utilizado para criar interfaces simples e rápidas para visualização de dados.  

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
* `src/airflow/dags/resources/` - Arquivo de conexão com o MinIO e demais funcionalidades de coleta e inserção.
* `src/airflow/dags/scrapy/` - Arquivo principal com a respagem de dados do projeto.
* `src/airflow/dags/` - Arquivo endereçados como Bronze, Silver e Gold, que é o core do projeto com a DAG para orquestração do processo.
* `tests/` - Arquivo que propõe teste unitários em classes e métodos.


## Estrutura de Pastas

```bash
|
|── .devcontainer/
|── .dockerignore
|── .docker-compose.yml
|── .gitignore
|── .python-version
|── requirements.txt
|── poetry.lock
|── pyproject.toml
|── README.md
|── assets/
|── config_airflow/
|   └── airflow.Dockerfile
|── data/
|── docs/
|── frontend/
|   |── components/
|   |       |── footer.py
|   |       └── inputs_css.py
|   |── configs/
|   |       └── settings_page.py
|   |── app.py
|   |── Dockerfile.py
|   └── requirements.txt
|── notebook/
|── src/
|   └── airflow/
|          └── dags/
|                |── resources/
|                |   |── __init__.py
|                |   └── minio_manager.py
|                |── scrapy/
|                |   |── __init__.py
|                |   |── collect.py
|                |   └── paramns.py
|                |── tools/
|                |   |── transform.py
|                |   └── rules_gold.py
|                |── __init__.py
|                |── bronze.py
|                |── silver.py
|                |── gold.py
|                └── TaskGroup.py
|
└── tests/
        |── test_1.py
        └── test_2.py
```

## Setup do Projeto

#### **1. Clone o repositório**
```bash
> git clone https://github.com/imbrunoagc/data-resident-evil.git
> cd data-resident-evil
```

#### **2. Execute o projeto**
```bash
> docker-compose up --build
``` 

## Setup de execução do projeto em Docker
Como o projeto está construido em serviços docker, o que é preciso para levantar os serviços é `docker-compose up`, agora quando subir e você acessar o caminho http://127.0.0.1:9001/ em seu navegador. verá que vai existir 1 bucket com as seguintes camadas `bronze, silver e gold`.

Agora, faça um ``docker-compose down -v``, para derrubar os serviços e deletar os volumes.

Após derrubar os volumes, caso deseje realizar a delete das imagens só realizar os seguintes comandos:
1. Visualizar as imagens
```bash
docker images
```
![alt text](assets/docker-images.png)

2. Comando para deletar a imagem por **IMAGE ID**
```bash
docker rmi IMAGE ID
```
![alt text](assets/docker-rmi-images.png)

3. Acessar o ambiente do airflow para executar a ``DAG``.

* Através do ambiente do docker-desktop acesse o ``airflow`` -> ``files/``.
* Abra o arquivo ``standalone_admin_password.txt`` no diretório ``opt/airflow`` e guarde a chave em um local seguro.
* Acesse a porta do airflow atraves do navegador desejado.
* user: admin
* password: conteudo armazenado no arquio ``standalone_admin_password.txt``

## Métricas e Regras | Gold

| **Métrica**                     | **Cálculo/Regra**                                                                 | **Gold? (Sim/Não)**                                                                                                        |
|----------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| **Top Personagens Populares**   | Ordenar por `aparicoes` e selecionar os top N (ex: top 10).                       | **Sim** - Uma visão consolidada e resumida que agrega dados de outras camadas.                                            |
| **Distribuição por Tipo Sanguíneo** | Contar o número de personagens por `tipo_sanguineo`.                                | **Sim** - Agrega dados categóricos que podem ser usados em análises e dashboards.                                         |
| **Média de Altura por Tipo Sanguíneo** | Calcular `mean(altura)` agrupando por `tipo_sanguineo`.                              | **Sim** - Transformação de dados brutos para uma métrica consolidada.                                                    |
| **Média de Peso por Tipo Sanguíneo** | Calcular `mean(peso)` agrupando por `tipo_sanguineo`.                                | **Sim** - Métrica consolidada para análises específicas.                                                                 |
| **Altura x Peso (Scatter)**     | Não há agregação; apenas exibição individual dos dados (gráfico de dispersão).     | **Não** - Dados brutos, melhor na camada **Silver** para análise exploratória.

## Como executar o ruff?

```bash
# Execução para verificar o código
> ruff check .

# Execução para verificar o código e corrigir
> ruff check . --fix
```

## Como executar o pytest?


## Como executar o Streamlit?
```bash
# Para execução local, basta seguir com a instalação do pacote stramlit
> pip install streamlit | poetry add streamlit

# Execução local
> streamlit run app.py
```

# Screenshot

## MiniIO

- 1. Bucket Criado.
<table>
    <td>
    <img src="assets/minIO-buckets.png"
></img></td></tr>
</table>

- 2. Camadas do medallion.
<table>
    <td>
    <img src="assets/minIO-layers.png"
></img></td></tr>
</table>

- 3. Registros na camada Bronze no formato **JSON**.
<table>
    <td>
    <img src="assets/minIO-records-bronze.png"
></img></td></tr>
</table>

- 4. Registros na camada Silver no formato **PARQUET**.
<table>
    <td>
    <img src="assets/minIO-records-silver.png"
></img></td></tr>
</table>

- 5. Registros na camada Gold agregados/sumarizados no formato **PARQUET**.
<table>
    <td>
    <img src="assets/minIO-records-gold.png"
></img></td></tr>
</table>

## Demo App
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://data-resident-evil-wkwerqngfdjhsbsgrfyvzn.streamlit.app/)

## Colab notebook graphics
[![Colab Notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/imbrunoagc/data-resident-evil/blob/main_medellion/notebook/visualize_data_gold.ipynb)
