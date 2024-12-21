import pg8000
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Charger les variables d'environnement
load_dotenv()

# Paramètres de connexion
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Fonction pour établir une connexion
def get_connection():
    return pg8000.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        ssl_context=True  # Activer SSL
    )
