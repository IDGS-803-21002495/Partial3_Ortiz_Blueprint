from flask import Flask, render_template, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_login import LoginManager, login_required, login_manager
from models import db, Usuario

# Importar blueprints 
from controller.auth import auth_bp
from controller.pedidos import pedidos_bp
from controller.clientes import cliente_bp
from controller.proveedores import proveedores_bp
from controller.usuarios import usuario_bp


app = Flask(__name__)
csrf = CSRFProtect()
app.config.from_object(DevelopmentConfig)

# Configuracion Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(proveedores_bp)
app.register_blueprint(usuario_bp)

# Iniciar aplicación en el Login 
@app.route("/")
def home():
    return redirect(url_for("auth.login"))

if __name__ == '__main__':

    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)