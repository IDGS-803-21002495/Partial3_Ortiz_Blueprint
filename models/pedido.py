from models import db
import datetime

# tabla de pedidos
class Pedido(db.Model):
    __tablename__='pedidos'
    id=db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(70), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    fecha_pedido = db.Column(db.DateTime,default = datetime.datetime.now)