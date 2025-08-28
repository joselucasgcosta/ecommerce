import jaydebeapi
import jpype
from queue import Queue
from config import Config
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OracleConnection:
    def __init__(self):
        self.config = Config()
        self.pool = None
        self.jdbc_driver = self.config.JDBC_DRIVER_NAME
        self.jdbc_jar = self.config.JDBC_JAR_PATH
        self.jdbc_url = self.config.JDBC_URL
        self.min_pool = 2
        self.max_pool = 10

        self._start_jvm()

    def _start_jvm(self):
        """Inicia a JVM para uso do JDBC"""
        try:
            if not jpype.isJVMStarted():
                jpype.startJVM(classpath=[self.jdbc_jar])
                logger.info("✅ JVM iniciada com sucesso para JDBC.")
        except Exception as e:
            logger.error(f"Erro ao iniciar JVM: {e}")
            raise

    def create_pool(self):
        """Cria um pool de conexões JDBC (simulado com Queue)"""
        try:
            self.pool = Queue(maxsize=self.max_pool)
            for _ in range(self.min_pool):
                conn = self._create_connection()
                self.pool.put(conn)
            logger.info(f"✅ Pool JDBC criado com {self.min_pool} conexões.")
            return True
        except Exception as e:
            logger.error(f"Erro ao criar pool JDBC: {e}")
            return False

    def _create_connection(self):
        """Cria uma nova conexão JDBC"""
        try:
            conn = jaydebeapi.connect(
                self.jdbc_driver,
                self.jdbc_url,
                [self.config.ORACLE_USER, self.config.ORACLE_PASSWORD]
            )
            return conn
        except Exception as e:
            logger.error(f"Erro ao criar conexão JDBC: {e}")
            raise

    def get_connection(self):
        """Obtém uma conexão do pool (ou cria nova se pool não estiver pronto)"""
        if not self.pool:
            if not self.create_pool():
                return None
        try:
            if self.pool.empty():
                logger.warning("⚠ Pool vazio, criando nova conexão JDBC.")
                return self._create_connection()
            return self.pool.get()
        except Exception as e:
            logger.error(f"Erro ao obter conexão JDBC: {e}")
            return None

    def release_connection(self, conn):
        """Devolve a conexão ao pool"""
        try:
            if self.pool.qsize() < self.max_pool:
                self.pool.put(conn)
            else:
                conn.close()
        except Exception as e:
            logger.error(f"Erro ao devolver conexão ao pool: {e}")

    def execute_query(self, query, params=None):
        """Executa uma query e retorna os resultados com tipos Python"""
        connection = self.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()
            cursor.execute(query, params or [])
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            result = []
            for row in rows:
                # Converte tipos Java para Python nativos
                converted_row = []
                for value in row:
                    if hasattr(value, "toString"):
                        value = str(value)  # Converte objetos Java para string
                    elif isinstance(value, (int, float, str, bool)) or value is None:
                        pass  # Já é tipo Python nativo
                    else:
                        try:
                            value = str(value)
                        except:
                            value = None
                    converted_row.append(value)

                result.append(dict(zip(columns, converted_row)))

            return result

        except Exception as e:
            logger.error(f"Erro ao executar query JDBC: {e}")
            return None
        finally:
            cursor.close()
            self.release_connection(connection)


# Instância global
oracle_db = OracleConnection()