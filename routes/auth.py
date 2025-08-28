from flask import Blueprint, request, jsonify, session
from models.oracle_models import ClienteOracle
from models.user import User
import logging

# Configurar logging para ver as mensagens no console do Flask
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        cnpj = data.get('cnpj')
        
        logger.info(f"Tentativa de login para CNPJ: {cnpj}")
        
        if not cnpj:
            logger.warning("CNPJ não fornecido na requisição.")
            return jsonify({'error': 'CNPJ é obrigatório'}), 400
        
        # Buscar cliente no Oracle
        cliente = ClienteOracle.get_by_cnpj(cnpj)
        
        if not cliente:
            logger.warning(f"Cliente com CNPJ {cnpj} não encontrado no Oracle.")
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        # Verificar se cliente está bloqueado
        if cliente['BLOQUEIO'] == None:
            logger.warning(f"Cliente {cliente['CODCLI']} ({cnpj}) está bloqueado.")
            return jsonify({'error': 'Cliente bloqueado'}), 403
        
        # Salvar dados do cliente na sessão
        session['cliente_id'] = cliente['CODCLI']
        session['cliente_nome'] = cliente['CLIENTE']
        session['limite_disponivel'] = float(cliente['LIMDISP'])
        session['filial'] = cliente['FILIAL']
        
        logger.info(f"Login bem-sucedido para cliente {cliente['CODCLI']} ({cnpj}).")
        
        return jsonify({
            'success': True,
            'cliente': {
                'id': cliente['CODCLI'],
                'nome': cliente['CLIENTE'],
                'cnpj': cnpj,
                'limite_credito': float(cliente['LIMCRED']),
                'limite_disponivel': float(cliente['LIMDISP']),
                'filial': cliente['FILIAL'],
                'uf': 'Minas Gerais' if cliente['FILIAL'] == 1 else 'Bahia'
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Erro durante o login: {e}", exc_info=True) # exc_info=True para ver o traceback completo
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    logger.info("Logout realizado com sucesso.")
    return jsonify({'success': True}), 200

# Rota do login para o manager
@auth_bp.route('/login/manager', methods=['POST'])
def login_admin():
    try:
        data = request.get_json()
        user_id = data.get('id')
        username = data.get('username')

        if not user_id:
            return jsonify({ "error": "ID não fornecido" }), 400

        user = User.query.filter_by(id=user_id).first()

        if user:
            # Salvar dados do cliente na sessão
            session['codacess'] = user.id
            session['username'] = user.username

            return jsonify({ "id": user.id, "username": user.username }), 200
        else:
            return jsonify({ "error": "Código inválido ou não autorizado" }), 401

    except Exception as e:
        logger.error(f"Erro durante o login: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
    
@auth_bp.route('/users/all', methods=['GET'])
def get_todos_usuarios():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
