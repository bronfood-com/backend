FROM python:3.11-slim

WORKDIR /app
COPY ./infra /app/infra/
COPY requirements.txt /app
COPY ./src/ /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
