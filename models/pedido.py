from datetime import datetime
from models.user import db

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, nullable=False)  # Removendo FK pois cliente está no Oracle
    data_pedido = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    observacoes = db.Column(db.Text, nullable=True)
    valor_total = db.Column(db.Float, nullable=False)
    valor_total_desconto = db.Column(db.Float, nullable=False)
    plano_pagamento = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    responsavel_id = db.Column(db.Integer, nullable=False)
    cliente_nome = db.Column(db.String(255), nullable=False)
    
    # Relacionamento com itens do pedido
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pedido {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente_nome,
            'data_pedido': self.data_pedido.isoformat() if self.data_pedido else None,
            'valor_total': self.valor_total,
            'valor_total_desconto': self.valor_total_desconto,
            'plano_pagamento': self.plano_pagamento,
            'status': self.status,
            'itens': [item.to_dict() for item in self.itens],
            'responsavel_id': self.responsavel_id
        }

class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    
    
    # Relacionamento com item
    item = db.relationship('Item', backref='pedido_itens')

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal,
            'item': self.item.to_dict() if self.item else None,
            'observacoes': self.observacoes
        }

