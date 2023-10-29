# config.py

import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Configuración de la base de datos usando las variables de entorno
DB_CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port':33065,
    'database': os.getenv('DB_DATABASE'),
    'raise_on_warnings': True
}
