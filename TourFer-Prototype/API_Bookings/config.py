import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "user_reservas")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "reservaspass456")
    MYSQL_DB = os.getenv("MYSQL_DB", "reservas_db")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_CURSORCLASS = "DictCursor"
    MYSQL_SSL_CA = os.getenv("MYSQL_SSL_CA", "ca.pem")

    CATALOGO_API_URL = os.getenv("CATALOGO_API_URL", "http://127.0.0.1:5001")

    CATALOGO_API_KEY = os.getenv("CATALOGO_API_KEY", "tourfer-catalogo-secret-key")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "tourfer12345")

def get_catalogo_api_config():
    return {
        "url": Config.CATALOGO_API_URL,
        "key": Config.CATALOGO_API_KEY
    }
