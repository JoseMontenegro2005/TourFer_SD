import MySQLdb
import os

def get_db_connection(config):
    """
    Crea una conexión a base de datos MySQL nativa compatible con 
    el código de app.py. Soporta SSL para Aiven.
    """
    
    # Configuramos SSL si existe el certificado (para Aiven)
    ssl_config = None
    # Verificamos si existe la config MYSQL_SSL_CA o si usas DB_SSL_CA
    ca_path = getattr(config, 'MYSQL_SSL_CA', None)
    
    if ca_path and os.path.exists(ca_path):
        ssl_config = {'ca': ca_path}
        print(f"Conectando con SSL usando: {ca_path}")

    # Intentamos obtener las variables, soportando ambos nombres (DB_... o MYSQL_...)
    host = getattr(config, 'MYSQL_HOST', getattr(config, 'DB_HOST', None))
    user = getattr(config, 'MYSQL_USER', getattr(config, 'DB_USER', None))
    password = getattr(config, 'MYSQL_PASSWORD', getattr(config, 'DB_PASSWORD', None))
    db_name = getattr(config, 'MYSQL_DB', getattr(config, 'DB_NAME', None))
    port = getattr(config, 'MYSQL_PORT', getattr(config, 'DB_PORT', 3306))

    conn = MySQLdb.connect(
        host=host,
        user=user,
        passwd=password,
        db=db_name,
        port=int(port),
        ssl=ssl_config # Aquí inyectamos la configuración SSL
    )
    
    return conn