from flask import Blueprint, request, jsonify, session
from models.user import db
from models.item import Item
from models.combo import Combo
from models.pedido import Pedido, ItemPedido
from models.oracle_models import ClienteOracle, PlanosPagamentoOracle
from datetime import datetime

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    try:
        # Verificar se cliente está logado
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'error': 'Cliente não autenticado'}), 401
        
        data = request.get_json()
        itens = data.get('itens', [])
        plano_pagamento_codigo = data.get('plano_pagamento')
        observacoes = data.get('observacoes', '')
        cliente_nome = data.get('cliente_nome')
        valor_total_desconto = data.get('valor_total_desconto')
        
        if not itens:
            return jsonify({'error': 'Nenhum item no pedido'}), 400
        
        responsavel_id = data.get('responsavel_id')
        if not responsavel_id:
            return jsonify({'error': 'Responsável pelo pedido é obrigatório'}), 400
        
        if not plano_pagamento_codigo:
            return jsonify({'error': 'Plano de pagamento é obrigatório'}), 400
        
        # Buscar dados do cliente no Oracle
        cliente = ClienteOracle.get_by_id(cliente_id)
        if not cliente:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        # Verificar se o plano de pagamento é válido para o cliente
        planos_cliente = PlanosPagamentoOracle.get_by_cliente(cliente_id)
        plano_valido = None
        for plano in planos_cliente:
            if plano['CODPLPAG'] == int(plano_pagamento_codigo):
                plano_valido = plano
                break
        
        if not plano_valido:
            return jsonify({'error': 'Plano de pagamento não disponível para este cliente'}), 400
        
        # Calcular valor total
        valor_total = 0
        for item_data in itens:
            if item_data.get('tipo') == 'combo':
                # Para combos, usar o preço do combo
                combo = Combo.query.get(item_data['id'])
                if combo:
                    valor_total += combo.preco_total * item_data['quantidade']
            else:
                # Para itens individuais
                item = Item.query.filter_by(id=item_data['id']).first()
                # item = Item.query.get(item_data['id']) ----> caso não tenha o id_cont
                if item:
                    valor_total += item.preco * item_data['quantidade']
        
        # Aplicar desconto se for à vista (assumindo que planos com 0 dias são à vista)
        desconto = 0
        if plano_valido['NUMDIAS'] == 0:
            desconto = valor_total * 0.0  # 5% de desconto
            valor_total -= desconto
        
        # Verificar limite de crédito
        status = "APROVADO"
        if valor_total > float(cliente['LIMDISP']):
            # return jsonify({'error': 'Valor excede o limite disponível'}), 400
            status = "BLOQUEADO"            

        pedido = Pedido(
            cliente_id=cliente_id,
            valor_total=valor_total,
            plano_pagamento=plano_valido['DESCRPLPAG'],
            data_pedido=datetime.utcnow(),
            observacoes=observacoes,
            responsavel_id=responsavel_id,
            status=status,
            cliente_nome=cliente_nome,
            valor_total_desconto=valor_total_desconto
        )
        
        db.session.add(pedido)
        db.session.flush()  # Para obter o ID do pedido
        
        # Adicionar itens ao pedido
        for item_data in itens:
            if item_data.get('tipo') == 'combo':
                combo = Combo.query.get(item_data['id'])
                if not combo:
                    return jsonify({'error': f'Combo {item_data["id"]} não encontrado'}), 404

                quantidade_combo = item_data['quantidade']

                for combo_item in combo.itens:
                    item = combo_item.item
                    total_qtd = combo_item.quantidade * quantidade_combo

                    if item.estoque < total_qtd:
                        return jsonify({'error': f'Estoque insuficiente para o item {item.nome} do combo'}), 400

                    item.estoque -= total_qtd

                    item_pedido = ItemPedido(
                        pedido_id=pedido.id,
                        item_id=item.id,
                        quantidade=total_qtd,
                        preco_unitario=item.preco,
                        subtotal=item.preco * total_qtd,
                    )
                    db.session.add(item_pedido)

            else:
                item = Item.query.filter_by(id=item_data['id']).first()
                # item = Item.query.get(item_data['id']) ----> caso não tenha o id_cont
                if not item:
                    return jsonify({'error': f'Item {item_data["id"]} não encontrado'}), 404

                if item.estoque < item_data['quantidade']:
                    return jsonify({'error': f'Estoque insuficiente para o item {item.nome}'}), 400

                item.estoque -= item_data['quantidade']

                item_pedido = ItemPedido(
                    pedido_id=pedido.id,
                    item_id=item.id,
                    quantidade=item_data['quantidade'],
                    preco_unitario=item.preco,
                    subtotal=item.preco * item_data['quantidade'],
                    observacoes=item.destaque_texto
                )
                db.session.add(item_pedido)

        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pedido criado com sucesso',
            'pedido': {
                'id': pedido.id,
                'valor_total': valor_total,
                'desconto': desconto,
                'plano_pagamento': plano_valido['DESCRPLPAG'],
                'data_pedido': pedido.data_pedido.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar pedido: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@pedidos_bp.route('/pedidos/<int:cliente_id>', methods=['GET'])
def get_pedidos_cliente(cliente_id):
    try:
        pedidos = Pedido.query.filter_by(cliente_id=cliente_id).all()
        return jsonify([pedido.to_dict() for pedido in pedidos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pedidos_bp.route('/pedidos', methods=['GET'])
def get_all_pedidos():
    try:
        pedidos = Pedido.query.all()
        return jsonify([pedido.to_dict() for pedido in pedidos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pedidos_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    try:
        pedido = Pedido.query.get_or_404(pedido_id)
        return jsonify(pedido.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

