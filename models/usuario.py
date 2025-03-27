from models import db

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

# tabla de usuarios
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String(255), nullable= False)
    nombre = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    rol = db.Column(db.String(20), nullable = False)

    # generar hash de contraseña
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # verificar que la contraseña es correcta
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # obtener id
    def get_id(self):
        return str(self.id)
    
    # obtener rol 
    def get_rol(self):
        return self.rol