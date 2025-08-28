from flask import Blueprint, request, jsonify
from models.pedido_ol import PedidoOL
from models.user import db

pedido_ol_bp = Blueprint('pedido_ol', __name__)

@pedido_ol_bp.route('/pedido-ol', methods=['POST'])
def salvar_pedido_ol():
    try:
        data = request.get_json()

        cnpj_id = data.get('cnpj_codcli')
        laboratorio = data.get('laboratorio')
        nomerep = data.get('representante_ol')
        valor = data.get('valor_pedido')
        responsavel = data.get('responsavel')
        brinde_id = data.get('brinde_id')
        quantidade = data.get('quantidade')

        # Validação simples
        if not cnpj_id or not laboratorio or not nomerep or valor is None or not responsavel:
            return jsonify({'error': 'Todos os campos são obrigatórios.'}), 400

        novo_pedido = PedidoOL(
            cnpj_id=cnpj_id,
            laboratorio=laboratorio,
            nomerep=nomerep,
            valor=valor,
            responsavel=responsavel,
            brinde_id=brinde_id,
            quantidade_brinde=quantidade
        )

        db.session.add(novo_pedido)
        db.session.flush()  # garante que o ID já foi gerado

        pedido_id = novo_pedido.id  # pega o ID antes do commit

        db.session.commit()

        return jsonify({
            'message': 'Pedido OL salvo com sucesso!',
            'id': pedido_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
