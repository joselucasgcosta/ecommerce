from flask import Blueprint, jsonify
from models.item import Item
from models.combo import Combo

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/itens', methods=['GET'])
def get_itens():
    """Rota para obter todos os itens ativos"""
    try:
        itens = Item.query.filter_by(ativo=True).all()
        return jsonify([item.to_dict() for item in itens]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/itens/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Rota para obter um item específico"""
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item não encontrado'}), 404
        
        return jsonify(item.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/combos', methods=['GET'])
def get_combos():
    """Rota para obter todos os combos ativos"""
    try:
        combos = Combo.query.filter_by(ativo=True).all()
        return jsonify([combo.to_dict() for combo in combos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/combos/<int:combo_id>', methods=['GET'])
def get_combo(combo_id):
    """Rota para obter um combo específico"""
    try:
        combo = Combo.query.get(combo_id)
        if not combo:
            return jsonify({'error': 'Combo não encontrado'}), 404
        
        return jsonify(combo.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

