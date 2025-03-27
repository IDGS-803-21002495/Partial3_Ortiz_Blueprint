from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .roles import require_role
from models import db
from sqlalchemy import func
import os, datetime
from models.pedido import Pedido
from flask import Blueprint
from forms.pedidos_forms import DeliveryForm

pedidos_bp = Blueprint('pedidos',__name__, url_prefix='/pedidos')


# inicializar el archivo 
def iniciar_archivo():
    archivo = open('pedidos.txt', 'w')
    archivo.close()

# guardar el pedido en el archivo 
def guardar_pedido(pedido):
    archivo = open('pedidos.txt', 'r')
    # Leer las lineas del archivo para darle un ID a cada pedido
    lineas = archivo.readlines()
    id_pedido = len(lineas) + 1
    archivo.close()

    archivo = open('pedidos.txt','a')
    pedido_str = f"ID: {id_pedido}, Nombre: {pedido['nombre']}, Direccion: {pedido['direccion']}, Telefono: {pedido['telefono']}, Tamanio: {pedido['tamanio']}, Ingredientes: {pedido['ingredientes']}, Numero de Pizzas: {pedido['numero_pizzas']}, Subtotal: {pedido['subtotal']}\n"
    archivo.write(pedido_str)
    archivo.close()

# organizar los pedidos del archivo para mostrarlos en la tabla
def cargar_pedidos():
    pedidos = []
    archivo = open('pedidos.txt', 'r')
    for linea in archivo:
        datos = linea.strip().split(', ')
        pedido = {}
        for dato in datos:
            clave, valor = dato.split(': ', 1)
            pedido[clave] = valor
        pedidos.append(pedido)
    
    archivo.close()
    return pedidos

# Quitar pizza de la tabla de pedidos
def eliminar_pedido(id_pedido):
    archivo = open('pedidos.txt', 'r')
    lineas = archivo.readlines()
    archivo.close()

    # escribir de nuevo pero sin la linea seleccionada
    archivo = open('pedidos.txt','w')
    for linea in lineas:
        if f"ID: {id_pedido}" not in linea:
            archivo.write(linea)
    archivo.close()

# calcular el total del pedido
def calcular_total_pedido():
    archivo = open('pedidos.txt', 'r')
    total = 0  

    for linea in archivo:
        datos = linea.strip().split(', ')
        subtotal = 0

        for dato in datos:
            if dato.startswith('Subtotal'):
                subtotal = int(dato.split(': ')[1])

        total += subtotal

    archivo.close()
    return total

# generar un pedido nuevo
@pedidos_bp.route('/pedidos', methods=['GET', 'POST'])
@login_required
@require_role(['admin', 'empleado','cliente'])
def pedidos():
    create_form = DeliveryForm(request.form)

    if current_user.rol == 'cliente':
        create_form.nombre.data = current_user.nombre
  
    if request.method == 'POST':
        if create_form.validate():
            # Recuperar los datos del formulario
            nombre = create_form.nombre.data
            direccion = create_form.direccion.data
            telefono = create_form.telefono.data
            numero_pizzas = int(create_form.numero_pizzas.data)
            tamanio = request.form.get('tamanio')
            ingredientes = request.form.getlist('ingredientes')

            # calcular subtotal
            precio_tamanio = int(tamanio)  # Chica=40, Mediana=80, Grande=120
            precio_ingredientes = len(ingredientes) * 10  # Cada ingrediente cuesta $10
            subtotal = (precio_tamanio + precio_ingredientes) * numero_pizzas

            # determinar el tamaño
            tamanio_presentacion = ''
            if tamanio == '40':
                tamanio_presentacion = 'Chica'
            elif tamanio == '80':
                tamanio_presentacion = 'Mediana'
            elif tamanio == '120':
                tamanio_presentacion = 'Grande'

            # crear el pedido
            pedido = {
                "nombre": nombre,
                "direccion": direccion,
                "telefono": telefono,
                "tamanio": tamanio_presentacion,
                "ingredientes": len(ingredientes),
                "numero_pizzas": numero_pizzas,
                "subtotal": subtotal
            }

            # guardar el pedido en el archivo
            guardar_pedido(pedido)

            
    # cargar los pedidos desde el archivo
    pedidos = cargar_pedidos()
    return render_template('pedidos.html', form=create_form, pedidos=pedidos)

# eliminar una pedido (pizza) por ID
@pedidos_bp.route('/eliminar_pedido/<int:id_pedido>', methods=['POST','GET'])
@login_required
@require_role(['admin', 'empleado','cliente'])
def eliminar(id_pedido):
    if request.method == 'POST':
        eliminar_pedido(id_pedido)
    create_form = DeliveryForm(request.form)
    pedidos = cargar_pedidos()
    return render_template('pedidos.html', form=create_form, pedidos=pedidos)

# registrar un pedido en la base de datos
@pedidos_bp.route('/registrar_pedido', methods=['GET', 'POST'])
@login_required
@require_role(['admin', 'empleado','cliente'])
def registrar_pedido():
    create_form = DeliveryForm(request.form)
    
    if request.method == 'POST' and create_form.validate():
        total = calcular_total_pedido()
        nombre = create_form.nombre.data
        direccion = create_form.direccion.data
        telefono = create_form.telefono.data

        # crear instancia del objeto pedido
        ped = Pedido(
            nombre=nombre,  
            direccion=direccion,
            telefono=telefono,
            total=total
        )

        # guardar en la base de datos
        db.session.add(ped)
        db.session.commit()

        # borrar registros del archivo de texto
        iniciar_archivo()

        if current_user.rol == 'cliente':
            flash(f"Pedido registrado correctamente. Total a pagar: ${total}", "success")
            create_form = DeliveryForm()  # Reiniciar el formulario
        else:
            flash(f"Pedido registrado correctamente. Total a pagar: ${total}", "success")
            return redirect(url_for('pedidos.ver_pedidos'))

    return render_template('pedidos.html', form=create_form)

# ver todos los pedidos hechos y filtrar por mes o día
@pedidos_bp.route("/ver_pedidos", methods=['GET', 'POST'])
@login_required
@require_role(['admin', 'empleado'])
def ver_pedidos():
    create_form = DeliveryForm(request.form)
    pedidos = Pedido.query.all()
    total_ventas = 0.0

    if request.method == 'POST':
        tipo_busqueda = request.form.get('tipo_busqueda')
        fecha_input = request.form.get('fecha')

        # buscar por día
        if tipo_busqueda == 'dia':
            pedidos = Pedido.query.filter(func.date(Pedido.fecha_pedido) == fecha_input).all()
        # buscar por mes
        if tipo_busqueda == 'mes':
            anio, mes, dia = fecha_input.split('-')
            pedidos = Pedido.query.filter(
                func.year(Pedido.fecha_pedido) == int(anio),
                func.month(Pedido.fecha_pedido) == int(mes)
            ).all()

    total_ventas = sum([pedido.total for pedido in pedidos])

    return render_template("ver_pedidos.html", form = create_form, pedidos = pedidos, total_ventas = total_ventas)