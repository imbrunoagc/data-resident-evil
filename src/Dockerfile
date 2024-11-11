FROM python:3.12.2

WORKDIR /app

# Copie apenas o arquivo requirements.txt inicialmente
COPY requirements.txt requirements.txt

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Agora copie todo o código da pasta src
COPY . .

# Defina o comando padrão como vazio, já que o docker-compose especificará os scripts a serem executados
CMD ["python3", "bronze.py"]
