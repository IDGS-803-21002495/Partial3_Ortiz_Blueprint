from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.pedido import Pedido
from models.usuario import Usuario
from models.cliente import Cliente
from models.proveedor import Proveedor