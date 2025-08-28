from flask import Blueprint, jsonify, session
from models.oracle_models import ClienteOracle, PlanosPagamentoOracle

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/cliente/info', methods=['GET'])
def get_cliente_info():
    """Retorna informações do cliente logado"""
    try:
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'error': 'Cliente não autenticado'}), 401
        
        cliente = ClienteOracle.get_by_id(cliente_id)
        if not cliente:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        return jsonify({
            'id': cliente['CODCLI'],
            'nome': cliente['CLIENTE'],
            'cnpj': cliente['CGCENT'],
            'limite_credito': float(cliente['LIMCRED']),
            'limite_disponivel': float(cliente['LIMDISP']),
            'bloqueio': cliente['BLOQUEIO'],
            'filial': cliente['FILIAL']
        }), 200
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/cliente/planos-pagamento', methods=['GET'])
def get_planos_pagamento():
    """Retorna planos de pagamento disponíveis para o cliente logado"""
    try:
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'error': 'Cliente não autenticado'}), 401
        
        planos = PlanosPagamentoOracle.get_by_cliente(cliente_id)
        
        # Formatar planos para o frontend
        planos_formatados = []
        for plano in planos:
            planos_formatados.append({
                'codigo': plano['CODPLPAG'],
                'descricao': plano['DESCRPLPAG'],
                'dias': plano['NUMDIAS'],
                'parcelas': plano['NUMPARCELAS'],
                'prazo1': plano['PRAZO1'],
                'prazo2': plano['PRAZO2'],
                'prazo3': plano['PRAZO3'],
                'prazo4': plano['PRAZO4']
            })
        
        return jsonify(planos_formatados), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

