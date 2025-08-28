from flask import Blueprint, jsonify
from models.brinde import Brinde

brindes_bp = Blueprint('brindes', __name__)

@brindes_bp.route('/brindes', methods=['GET'])
def get_all_brindes():
    """Retorna todos os brindes cadastrados"""
    try:
        brindes = Brinde.query.all()

        if not brindes:
            return jsonify({'message': 'Nenhum brinde encontrado'}), 404

        brinde_list = []
        for brinde in brindes:
            brinde_list.append({
                'brinde_id': brinde.brinde_id,
                'brinde': brinde.brinde,
                'estoque': brinde.estoque,
                'valor': brinde.valor
            })

        return jsonify({'brindes': brinde_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500