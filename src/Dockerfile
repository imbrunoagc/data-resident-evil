FROM python:3.12.2

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#ENV ENDPOINT=http://minio:9000
#ENV ACCESS_KEY=minioadmin
#ENV SECRET_KEY=minioadmin

CMD ["python3"]
