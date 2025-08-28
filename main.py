import os
import sys
from config import Config
import jpype
import jaydebeapi
from flask import Flask, send_from_directory
from flask_cors import CORS
from models.user import db
from routes.user import user_bp
from routes.auth import auth_bp
from routes.produtos import produtos_bp
from routes.clientes import clientes_bp
from routes.pedidos import pedidos_bp
from routes.pedido_ol import pedido_ol_bp
from routes.brindes import brindes_bp

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Caminho do arquivo JDBC
jdbc_jar_path = Config.JDBC_JAR_PATH
jdbc_drver_name = Config.JDBC_DRIVER_NAME

db_host = Config.ORACLE_HOST
db_port = Config.ORACLE_PORT
db_service = Config.ORACLE_SERVICE
db_user = Config.ORACLE_USER
db_password = Config.ORACLE_PASSWORD
connection_sring = f"jdbc:oracle:thin:@//{db_host}:{db_port}/{db_service}"

# Função para iniciar a JVM e conectar
def get_connection():
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=jdbc_jar_path)
    return jaydebeapi.connect(jdbc_drver_name, connection_sring, [db_user, db_password])

# Teste rápido
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SYSDATE FROM DUAL")
    print("Conectado ao Oracle via JDBC:", cursor.fetchall())
    cursor.close()
    conn.close()
except Exception as e:
    print("Erro na conexão JDBC:", e)

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(produtos_bp, url_prefix='/api')
app.register_blueprint(clientes_bp, url_prefix='/api')
app.register_blueprint(pedidos_bp, url_prefix='/api')
app.register_blueprint(pedido_ol_bp, url_prefix='/api')
app.register_blueprint(brindes_bp, url_prefix='/api')

postgre_user = Config.POSTGRE_USER
postgre_password = Config.POSTGRE_PASSWORD

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgre_user}:{postgre_password}@localhost:5432/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    # Para ambientes de teste descomente a linha abaixo
    # init_sample_data()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
