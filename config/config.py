from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}

DIRECTORY_PATH = os.getenv('DIRECTORY_PATH')