from wtforms import Form

from wtforms import StringField, validators, PasswordField, EmailField, SelectField

class UsuarioForm(Form):
    Nombre = StringField('Nombre',[
        validators.DataRequired(message='Campo requerido.'),
        validators.Length(min=5, max=75, message='Ingrese un nombre válido')
    ])
    Username = StringField('Username',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=20, message='Ingrese un nombre de usuario válido')
    ])
    Contraseña = PasswordField('Contraseña',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=10, max=70, message='Ingrese una contraseña válida')
    ])
    Email = EmailField('Email',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=15, max=70, message='Ingrese un correo electronico válido')
    ])
    Rol = SelectField('Rol', choices=[
        ('admin', 'Administrador'),
        ('empleado', 'Empleado')
    ], validators=[validators.DataRequired(message='Seleccione un rol')])