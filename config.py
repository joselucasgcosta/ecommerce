import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Configuração PostgreSQL (para produtos e pedidos)
    POSTGRE_HOST = os.environ.get('POSTGRE_HOST', "postgres")
    POSTGRE_USER = os.environ.get('POSTGRE_USER', "postgres")
    POSTGRE_DB = os.environ.get('POSTGRE_DB', "app")
    POSTGRE_PASSWORD = os.environ.get('POSTGRE_PASSWORD', "postgres")
    POSTGRE_DATABASE_URI = f'postgresql://{POSTGRE_USER}:{POSTGRE_PASSWORD}@{POSTGRE_HOST}:5432/{POSTGRE_DB}'
    
    # Configuração Oracle (para clientes e planos de pagamento)
    ORACLE_HOST = os.environ.get('ORACLE_HOST')
    ORACLE_PORT = os.environ.get('ORACLE_PORT')
    ORACLE_SERVICE = os.environ.get('ORACLE_SERVICE')
    ORACLE_USER = os.environ.get('ORACLE_USER')
    ORACLE_PASSWORD = os.environ.get('ORACLE_PASSWORD')
    JDBC_JAR_PATH = os.environ.get('JDBC_JAR_PATH')
    JDBC_URL = os.environ.get('JDBC_URL')
    JDBC_DRIVER_NAME=os.environ.get('JDBC_DRIVER_NAME')
    
    @property
    def ORACLE_DSN(self):
        return f"{self.ORACLE_HOST}:{self.ORACLE_PORT}/{self.ORACLE_SERVICE}"

