import os


DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
DB_SERVER = os.getenv('POSTGRES_SERVER', 'localhost')
DB_NAME = os.getenv('POSTGRES_DB', 'fastapi_pets_db')
