from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from forms.proveedores_forms import ProveedorForm
from models import db
from models.proveedor import Proveedor
from flask import Blueprint
from .roles import require_role

proveedores_bp = Blueprint('proveedores',__name__, url_prefix='/proveedores')


@proveedores_bp.route('/todos',methods=['GET'])
@require_role(['admin'])
@login_required
def todos():
    create_form = ProveedorForm(request.form)
    proveedores = Proveedor.query.filter(Proveedor.estado == 'ACTIVO')
    return render_template('proveedores.html', form = create_form, proveedores = proveedores)

@proveedores_bp.route('/guardar', methods=['GET', 'POST'])
@require_role(['admin'])
@login_required
def guardar():
    create_form = ProveedorForm(request.form)
    
    if request.method == 'POST' and create_form.validate():
        nombre = create_form.Nombre.data
        direccion = create_form.Direccion.data
        telefono = create_form.Telefono.data
        email = create_form.Email.data

        # crear instancia del objeto 
        prov = Proveedor(
            nombre = nombre,
            direccion = direccion,
            telefono = telefono,
            email = email
        )

        db.session.add(prov)
        db.session.commit()
        # mostrar mensaje informando el total
        flash(f"Proveedor registrado correctamente", "success")
        return redirect(url_for('proveedores.todos'))

    return render_template('detalles_proveedor.html', form = create_form)

@proveedores_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
@require_role(['admin'])
@login_required
def eliminar(id):
    proveedor = Proveedor.query.get_or_404(id)
    proveedor.estado = 'INACTIVO'
    db.session.commit()
    flash(f"Proveedor {proveedor.nombre} eliminado correctamente.", "success")    
    return redirect(url_for('proveedores.todos'))

@proveedores_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
@login_required
def actualizar(id):
    proveedor = Proveedor.query.get_or_404(id)  
    create_form = ProveedorForm(request.form) 

    if request.method == 'POST' and create_form.validate():
        proveedor.nombre = create_form.Nombre.data
        proveedor.direccion = create_form.Direccion.data
        proveedor.telefono = create_form.Telefono.data
        proveedor.email = create_form.Email.data

        db.session.commit()
        flash(f"Proveedpr actualizado correctamente", "success")

        return redirect(url_for('proveedores.todos'))

    create_form.Nombre.data = proveedor.nombre
    create_form.Direccion.data = proveedor.direccion
    create_form.Telefono.data = proveedor.telefono
    create_form.Email.data = proveedor.email

    return render_template('actualizar_proveedor.html', form=create_form, proveedor=proveedor)
