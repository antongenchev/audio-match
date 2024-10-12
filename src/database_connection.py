import psycopg2
import os


def get_db_connection():
    '''
    Get a connection to the database
    '''
    print('environment variables:    ', os.getenv('POSTGRES_DB'), os.getenv('POSTGRES_USER'),os.getenv('POSTGRES_PASSWORD'),os.getenv('DB_HOST'),os.getenv('DB_PORT'))
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return connection
    except Exception as e:
        print(f'Error while connecting to the database: {e}')
