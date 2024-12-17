FROM python:3.12.2
WORKDIR /app/frontend
COPY requirements-frontend.txt /app/frontend/requirements-frontend.txt
RUN pip install --no-cache-dir --upgrade -r requirements-frontend.txt
COPY . /app/frontend
ENTRYPOINT ["streamlit", "run", "app.py"]