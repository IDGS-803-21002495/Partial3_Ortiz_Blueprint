from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from models import db
from models.usuario import Usuario
from flask import Blueprint
from .roles import require_role
from forms.usuarios_forms import UsuarioForm
usuario_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuario_bp.route('/todos', methods=['GET'])
@require_role(['admin'])
@login_required
def todos():
    create_form = UsuarioForm(request.form)
    usuarios = Usuario.query.filter()
    return render_template('usuarios.html', form = create_form, usuarios = usuarios)

@usuario_bp.route('/guardar', methods=['GET', 'POST'])
@require_role(['admin'])
@login_required
def guardar():
    create_form = UsuarioForm(request.form)
    
    if request.method == 'POST' and create_form.validate():
        nombre = create_form.Nombre.data
        username = create_form.Username.data
        password = create_form.Contraseña.data
        email = create_form.Email.data
        rol = create_form.Rol.data

        password_hash = generate_password_hash(password)

        # crear instancia del objeto 
        user = Usuario(
            nombre = nombre,
            username = username,
            password = password_hash,
            email = email,
            rol = rol
        )

        db.session.add(user)
        db.session.commit()
        # mostrar mensaje informando el total
        flash(f"Usuario registrado correctamente", "success")
        return redirect(url_for('usuarios.todos'))

    return render_template('detalles_usuario.html', form = create_form)
