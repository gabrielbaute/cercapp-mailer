import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    # Configuración común (si es necesario)
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Información de la aplicación
    APP_NAME = 'Cercapp'
    APP_URL = os.getenv('APP_URL', 'http://localhost:5000')
    VERSION = '0.1.0'

    # Credenciales del admin inicial
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@cercapp.us')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin1234')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/cercapp_mailer.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Encriptado
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_segura'
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    RESET_TOKEN_EXP_MINUTES = int(os.getenv('RESET_TOKEN_EXP_MINUTES', 25))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 30)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 30)))

    # Configuración de email general
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@cercapp.us')
    MAIL_BCC = ["contactocercapp@gmail.com"]

class ConfigCercapp(Config):
    """Clase CERCAPP para el uso del script de envíos de email masivos."""
    
    # Configuración de la app
    TEMPLATE_FOLDER = 'src/templates/'
    CONTACTS_CSV = 'data/contactos.csv'
    CONTACTOS_COMPLETAR_REGISTRO = 'data/completar_registro.csv'
    CONTACTOS_PRIMER_APORTE = 'data/primer_aporte.csv'
    CONTACTOS_INCENTIVO = 'data/todos.csv'
    PRUEBA='data/prueba.csv'

    @staticmethod
    def get_bcc_list():
        # Puedes expandir esto para leer de una DB o variable de entorno
        return ConfigCercapp.MAIL_BCC

class ConfigSaludFinanciera(Config):
    """Clase Dr. Salud Financiera para el uso del script de envíos de email masivos."""

    # Reescribe variables de email
    MAIL_SERVER = os.getenv('SALUD_FINANCIERA_MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('SALUD_FINANCIERA_MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('SALUD_FINANCIERA_MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('SALUD_FINANCIERA_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('SALUD_FINANCIERA_MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('SALUD_FINANCIERA_MAIL_DEFAULT_SENDER', 'no-reply@drsaludfinanciera.com')
    MAIL_BCC = ["contactocercapp@gmail.com"]
    
    # Configuración de la app
    TEMPLATE_FOLDER = 'templates'
    CONTACTS_CSV_1 = 'data/leads_1.csv'
    CONTACTS_CSV_2 = 'data/leads_2.csv'
    CONTACTS_CSV_3 = 'data/leads_3.csv'
    PRUEBA='data/prueba.csv'

    @staticmethod
    def get_bcc_list():
        # Puedes expandir esto para leer de una DB o variable de entorno
        return ConfigSaludFinanciera.MAIL_BCC