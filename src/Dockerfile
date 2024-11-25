FROM python:3.12.2
WORKDIR /app/src
COPY requirements.txt /app/src/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/src
CMD ["python3"]