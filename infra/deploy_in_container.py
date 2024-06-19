import logging
import os
import time
import subprocess

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
            user=os.getenv('POSTGRES_USER'),
        )
        logger.debug('Successful connection')
        break
    except psycopg2.OperationalError:
        logger.info('No connection to database, connection restarted')
        time.sleep(5)
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

# Создание моков
os.system('python manage.py create_mock_clients')
os.system('python manage.py create_mock_meals')
os.system('python manage.py create_mock_restaurants')

# Создание суперпользователя
superuser_script = """
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('0123456789', '0123456789', 'admin')
"""
try:
    subprocess.run(['python', 'manage.py', 'shell'], input=superuser_script, text=True, check=True)
    logger.info('Superuser created successfully')
except subprocess.CalledProcessError as e:
    logger.error('Error occurred during superuser creation:')
    logger.error(e.output)

# Сборка статики с выводом результатов в терминал
try:
    collectstatic_output = subprocess.check_output(['python', 'manage.py', 'collectstatic', '--noinput'], stderr=subprocess.STDOUT)
    logger.info(collectstatic_output.decode())
except subprocess.CalledProcessError as e:
    logger.error('Error occurred during collectstatic command execution:')
    logger.error(e.output.decode())
# os.system('python manage.py collectstatic --noinput')

# Дополнительная задержка для уверенности в завершении сборки статики
time.sleep(5)
# TODO Написать скрипт команды на создание суперпользователя и запустить его тут
os.system('gunicorn bronfood.wsgi:application --bind 0:8000')
