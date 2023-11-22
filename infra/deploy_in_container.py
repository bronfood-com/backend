import logging
import os
import time

import psycopg2
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

logger.debug('Waiting for database connection')
while True:
    try:
        psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            password=os.getenv('POSTGRES_PASSWORD'),
            user=os.getenv('POSTGRES_USER')
        )
        logger.debug('Successful connection')
        break
    except psycopg2.OperationalError:
        logger.info('No connection to database, connection restarted')
        time.sleep(5)
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')
# TODO: os.system('python manage.py collectstatic --noinput')
os.system('gunicorn bronfood.wsgi:application --bind 0:8000')
