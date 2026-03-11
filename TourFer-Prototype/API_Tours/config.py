import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "user_catalogo")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "tourpass123")
    MYSQL_DB = os.getenv("MYSQL_DB", "catalogo_db")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_CURSORCLASS = "DictCursor"
    MYSQL_SSL_CA = os.getenv("MYSQL_SSL_CA", "ca.pem")
    
    API_KEY = os.getenv("API_KEY", "tourfer-catalogo-secret-key")
# ...
    MYSQL_SSL_DISABLED = False
    
    MYSQL_SSL = {'ssl': {'ca': '/etc/ssl/cert.pem'}} 
def get_api_key():
    return Config.API_KEY
