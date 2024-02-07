import logging
import os
import time
from argparse import ArgumentParser, ArgumentTypeError

import psycopg2
from dotenv import load_dotenv
import redis
import requests

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def run_web():
    logger.debug('Waiting for PostgreSQL connection...')
    while True:
        try:
            connection = psycopg2.connect(
                host=os.getenv('DB_HOST') if args.prod else 'localhost',
                port=os.getenv('DB_PORT'),
                password=os.getenv('POSTGRES_PASSWORD'),
                user=os.getenv('POSTGRES_USER'),
            )
            connection.close()
            logger.debug('Successful connection')
            break
        except psycopg2.OperationalError:
            logger.info('No connection to PostgreSQL, connection restarted.')
            time.sleep(5)
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')
    # TODO: os.system('python manage.py collectstatic --noinput')
    os.system('gunicorn bronfood.wsgi:application --bind 0:8000')


def waiting_redis():
    logger.debug('Waiting for Redis connection...')
    while True:
        try:
            redis.Redis(
                host=os.getenv('RD_HOST') if args.prod else 'localhost'
            ).ping()
            logger.debug('Successful connection')
            break
        except redis.ConnectionError:
            logger.info('No connection to Redis, connection restarted.')
            time.sleep(5)


def waiting_web():
    logger.debug('Waiting for Web connection')
    while True:
        try:
            if requests.get(
                f'http://{os.getenv("DJ_HOST") if args.prod else "localhost"}:'
                f'{os.getenv("DJ_PORT")}/healthcheck/'
            ).status_code == requests.codes.OK:
                break
            logger.debug('Endpoint /healthcheck/ is not available.')
        except requests.exceptions.ConnectionError:
            logger.debug('No connection to Web, connection restarted.')
            time.sleep(5)
    logger.debug('Successful connection')


def run_scheduler():
    waiting_redis()
    waiting_web()
    os.system('python manage.py crontab')


def run_workers():
    waiting_redis()
    waiting_web()
    os.system('python manage.py rundramatiq')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '--web', dest='func', action='store_const', const=run_web
    )
    parser.add_argument(
        '--scheduler', dest='func', action='store_const', const=run_scheduler
    )
    parser.add_argument(
        '--workers', dest='func', action='store_const', const=run_workers
    )
    parser.add_argument('-p', '--prod', action='store_true')
    args = parser.parse_args()
    if args.prod:
        os.environ['ENV_NAME'] = 'prod'
    if func := args.func:
        func()
    else:
        raise ArgumentTypeError(
            'Use required flags --web, --scheduler or --workers'
        )
