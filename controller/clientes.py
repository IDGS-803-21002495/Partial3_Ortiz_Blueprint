from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from forms.clientes_forms import ClienteForm
from models import db
from .roles import require_role
from models.cliente import Cliente

from flask import Blueprint

cliente_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@cliente_bp.route('/todos',methods=['GET'])
@require_role(['admin', 'empleado'])
@login_required
def todos():
    create_form = ClienteForm(request.form)
    clientes = Cliente.query.filter(Cliente.estado == 'ACTIVO')
    return render_template('clientes.html', form = create_form, clientes = clientes)

@cliente_bp.route('/guardar', methods=['GET', 'POST'])
@require_role(['admin', 'empleado'])
@login_required
def guardar():
    create_form = ClienteForm(request.form)
    
    if request.method == 'POST' and create_form.validate():
        nombre = create_form.Nombre.data
        ape_paterno = create_form.Apellido_paterno.data
        ape_materno = create_form.Apellido_materno.data
        direccion = create_form.Direccion.data
        telefono = create_form.Telefono.data

        # crear instancia del objeto 
        cli = Cliente(
            nombre = nombre,
            ape_paterno = ape_paterno,
            ape_materno = ape_materno,
            direccion = direccion,
            telefono = telefono
        )

        db.session.add(cli)
        db.session.commit()
        # mostrar mensaje informando el total
        flash(f"Cliente registrado correctamente", "success")
        return redirect(url_for('clientes.todos'))

    return render_template('detalles_cliente.html', form = create_form)

@cliente_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
@require_role(['admin', 'empleado'])
@login_required
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    cliente.estado = 'INACTIVO'
    db.session.commit()
    flash(f"Cliente {cliente.nombre} {cliente.ape_paterno} eliminado correctamente.", "success")    
    return redirect(url_for('clientes.todos'))

@cliente_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
@require_role(['admin', 'empleado'])
@login_required
def actualizar(id):
    cliente = Cliente.query.get_or_404(id)  
    create_form = ClienteForm(request.form) 

    if request.method == 'POST' and create_form.validate():
        cliente.nombre = create_form.Nombre.data
        cliente.ape_paterno = create_form.Apellido_paterno.data
        cliente.ape_materno = create_form.Apellido_materno.data
        cliente.direccion = create_form.Direccion.data
        cliente.telefono = create_form.Telefono.data

        db.session.commit()
        flash(f"Cliente actualizado correctamente", "success")

        return redirect(url_for('clientes.todos'))

    create_form.Nombre.data = cliente.nombre
    create_form.Apellido_paterno.data = cliente.ape_paterno
    create_form.Apellido_materno.data = cliente.ape_materno
    create_form.Direccion.data = cliente.direccion
    create_form.Telefono.data = cliente.telefono

    return render_template('actualizar_cliente.html', form=create_form, cliente=cliente)
