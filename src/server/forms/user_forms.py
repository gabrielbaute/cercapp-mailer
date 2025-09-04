from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class UserCreateForm(FlaskForm):
    """Formulario para crear un nuevo usuario"""
    
    username = StringField(
        'Nombre de usuario',
        validators=[DataRequired(message="El nombre de usuario es obligatorio."),
                    Length(min=3, max=25, message="El nombre de usuario debe tener entre 3 y 25 caracteres.")]
    )
    
    email = StringField(
        'Correo electrónico',
        validators=[DataRequired(message="El correo electrónico es obligatorio."),
                    Email(message="Por favor, introduce una dirección de correo electrónico válida.")]
    )
    
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message="La contraseña es obligatoria."),
                    Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")]
    )
    
    confirm_password = PasswordField(
        'Confirmar contraseña',
        validators=[DataRequired(message="Por favor, confirma tu contraseña."),
                    EqualTo('password', message="Las contraseñas deben coincidir.")]
    )
    
    submit = SubmitField('Crear usuario')

class UserUpdateForm(FlaskForm):
    """Formulario para actualizar un usuario existente"""
    
    username = StringField(
        'Nombre de usuario',
        validators=[DataRequired(message="El nombre de usuario es obligatorio."),
                    Length(min=3, max=25, message="El nombre de usuario debe tener entre 3 y 25 caracteres.")]
    )
    
    email = StringField(
        'Correo electrónico',
        validators=[DataRequired(message="El correo electrónico es obligatorio."),
                    Email(message="Por favor, introduce una dirección de correo electrónico válida.")]
    )
    
    submit = SubmitField('Actualizar usuario')