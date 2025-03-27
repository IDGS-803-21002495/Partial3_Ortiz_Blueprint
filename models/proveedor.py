from models import db
import datetime

# tabla de proveedores 
class Proveedor(db.Model):
    __tablename__='proveedor'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(70), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='ACTIVO') 
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.now)