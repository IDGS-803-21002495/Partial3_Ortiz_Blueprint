from wtforms import Form

from wtforms import StringField, validators

class ClienteForm(Form):
    Nombre = StringField('Nombre',[
        validators.DataRequired(message='Campo requerido.'),
        validators.Length(min=5, max=70, message='Ingrese un nombre válido')
    ])
    Apellido_paterno = StringField('Apellido_Paterno',[
        validators.DataRequired(message='Campo requerido.'),
        validators.Length(min=5, max=70, message='Ingrese un nombre válido')
    ])
    Apellido_materno = StringField('Apellido_Materno',[
        validators.DataRequired(message='Campo requerido.'),
        validators.Length(min=5, max=70, message='Ingrese un nombre válido')
    ])
    Direccion = StringField('Direccion',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=120, message='Ingrese una dirección válido')
    ])
    Telefono = StringField('Telefono',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=10, message='Ingrese un número telefonico válido')
    ])