from typing import Type
from src.config import Config
from flask import Flask

def create_script_app(config: type = Config) -> Flask:
    """
    Factory para crear la aplicación Flask para scripts
    Args:
        config: Clase de configuración a usar (por defecto Config)
    Returns:
        Instancia de Flask
    """
    
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates')
    app.config.from_object(config)
    
    return app