from models.user import db

class Brinde(db.Model):
    brinde_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brinde = db.Column(db.String(255), nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Item {self.brinde}>'

    def to_dict(self):
        return {
            'brinde_id': self.brinde_id,
            'brinde': self.brinde,
            'estoque': self.estoque,
            'valor': self.valor,
        }