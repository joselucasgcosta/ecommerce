from models.user import db

class PedidoOL(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cnpj_id = db.Column(db.Integer, nullable=False)
    laboratorio = db.Column(db.String(255), nullable=False)
    nomerep = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    responsavel = db.Column(db.String(255), nullable=False)
    brinde_id = db.Column(db.Integer, nullable=False)
    quantidade_brinde = db.Column(db.Integer, nullable=False)