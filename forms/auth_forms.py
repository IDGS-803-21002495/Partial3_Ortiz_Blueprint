from wtforms import Form

from wtforms import StringField, validators, PasswordField

class LoginForm(Form):
    Usuario = StringField('Usuario',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=3, max=20, message='Ingrese un nombre de usuario válido')
    ])
    Contraseña = PasswordField('Contraseña',[
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=5, max=30, message='Ingrese una contraseña válida')
    ])