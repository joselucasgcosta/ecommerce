from models.user import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    limite_credito = db.Column(db.Float, nullable=False)
    limite_disponivel = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cnpj': self.cnpj,
            'limite_credito': self.limite_credito,
            'limite_disponivel': self.limite_disponivel
        }

