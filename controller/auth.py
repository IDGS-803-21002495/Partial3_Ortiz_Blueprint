from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from forms.auth_forms import LoginForm
from models import db
from models.usuario import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# permitir acceso si el usuario esta registrado o denegar si no lo esta
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    create_form = LoginForm(request.form)
    if request.method == 'POST' and create_form.validate():
        username = create_form.Usuario.data
        password = create_form.Contraseña.data

        # recuperar el usuario que coincida con el username capturada
        user = Usuario.query.filter_by(username=username).first()

        hash = generate_password_hash(password)
        print(f"Hash de la contraseña: {hash}")

        # validar si la contraseña coincide con el username
        if user and user.check_password(password):  
            login_user(user)
            # Redirigir según el rol del usuario
            if user.rol == 'admin' or user.rol == 'empleado':
                return redirect(url_for('pedidos.ver_pedidos'))  
            elif user.rol == 'cliente':
                return redirect(url_for('pedidos.pedidos'))  
            else:
                flash("Usuario no reconocido", "danger")
        else:
            flash("Nombre de usuario o contraseña incorrectos", "danger")

    return render_template('login.html', form=create_form)

# salir de la aplicación
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        print('Sesión cerrada')
        return redirect('login')