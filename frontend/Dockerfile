# Dockerfile.frontend

# Imagem base
FROM python:3.12.2

# Copiar a pasta frontend e o arquivo app.py para o diretório /app do contêiner
COPY . /app/frontend

# Definir o diretório de trabalho no container
WORKDIR /app/frontend

# Instalção das dependencias de frontend
RUN pip install --no-cache-dir --upgrade -r /app/frontend/requirements-frontend.txt

ENTRYPOINT [ "streamlit", "run", "app.py" ]
# Comando para executar a aplicação
#CMD ["streamlit", "run", "app.py"]
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=127.0.0.1"]