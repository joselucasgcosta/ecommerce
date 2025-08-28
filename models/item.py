from models.user import db

class Item(db.Model):
    id = db.Column(db.Integer, nullable=False)
    id_cont = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    quantidade_promocao = db.Column(db.Integer, default=1)
    quantidade_max_promocao = db.Column(db.Integer, default=1)
    estoque = db.Column(db.Integer, default=1)
    imagem_url = db.Column(db.String(500))
    ativo = db.Column(db.Boolean, default=True)
    destaque = db.Column(db.Boolean, default=False)
    promocao = db.Column(db.Boolean, default=True)
    destaque_texto = db.Column(db.Text)
    laboratorio = db.Column(db.String(200), nullable=False)
    filial = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Item {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_cont': self.id_cont,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'quantidade_promocao': self.quantidade_promocao,
            'quantidade_max_promocao': self.quantidade_max_promocao,
            'estoque': self.estoque,
            'imagem_url': self.imagem_url,
            'ativo': self.ativo,
            'destaque': self.destaque,
            'promocao': self.promocao,
            'destaque_texto': self.destaque_texto,
            'laboratorio': self.laboratorio,
            'filial': self.filial
        }

