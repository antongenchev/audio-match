import psycopg2
import os


def get_db_connection():
    '''
    Get a connection to the database
    '''
    try:
        connection = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('DB_HOST')
        )
        return connection
    except Exception as e:
        print(f'Error while connecting to the database: {e}')
