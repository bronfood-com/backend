FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app
COPY ./src/ /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "bronfood.wsgi:application", "--bind", "0:8000"]
