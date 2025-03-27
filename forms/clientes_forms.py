from wtforms import Form

from wtforms import StringField, validators, EmailField, PasswordField

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
    Contraseña = PasswordField('Contraseña',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=10, max=70, message='Ingrese una contraseña válida')
    ])
    Email = EmailField('Email',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=15, max=70, message='Ingrese un correo electronico válido')
    ])