FROM python:3.12.2


# Copia o restante dos arquivos do projeto
COPY . /app/src

# Pasta de trabalho raiz no docker
WORKDIR /app/src

# Instala as dependências do projeto usando python
RUN pip install --no-cache-dir -r /app/src/requirements.txt

##### Copiar apenas src para que na leitura da funcao no fron, já exista a pasta src

CMD ["python3"]
#ENTRYPOINT [ "bash", "-c", "python bronze.py & python silver.py & python gold.py" ]