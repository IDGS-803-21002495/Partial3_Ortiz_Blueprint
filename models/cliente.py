from models import db
import datetime

# Tabla de clientes
class Cliente(db.Model):
    __tablename__='cliente'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(70))
    ape_paterno = db.Column(db.String(70), nullable=False)
    ape_materno = db.Column(db.String(70), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(10), nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='ACTIVO') 
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.now)