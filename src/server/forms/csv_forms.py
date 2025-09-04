from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class CSVUploadForm(FlaskForm):
    """Formulario para subir archivos CSV"""
    
    csv_file = FileField(
        'Archivo CSV',
        validators=[DataRequired(message="Por favor, selecciona un archivo CSV.")]
    )
    
    submit = SubmitField('Subir archivo')