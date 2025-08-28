from models.user import db

class Combo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    preco_total = db.Column(db.Float, nullable=False)
    imagem_url = db.Column(db.String(500))
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamento com itens do combo
    itens = db.relationship('ComboItem', backref='combo', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Combo {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco_total': self.preco_total,
            'imagem_url': self.imagem_url,
            'ativo': self.ativo,
            'itens': [item.to_dict() for item in self.itens]
        }

class ComboItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    combo_id = db.Column(db.Integer, db.ForeignKey('combo.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    
    # Relacionamento com item
    item = db.relationship('Item', backref='combo_itens')

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'quantidade': self.quantidade,
            'item': self.item.to_dict() if self.item else None
        }

