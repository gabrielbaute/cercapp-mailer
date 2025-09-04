import logging
from datetime import datetime
from flask import Flask

from src.config import Config, create_initial_admin
from src.server.routes import register_blueprints
from src.database import db, init_db
from src.server.server_extensions import init_login_manager, init_migrate, init_csrf
from src.utils import Banner
from src.cercapplogger import LoggerConfig

def create_app() -> Flask:
    """Factory para crear la aplicación Flask"""
    
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates')
    app.config.from_object(Config)

    init_db(app)
    init_migrate(app, db)
    init_login_manager(app)
    init_csrf(app)
    register_blueprints(app)

    with app.app_context():
        banner = Banner(Config.APP_NAME)
        banner.print_banner()
        db.create_all()
        create_initial_admin()
    
    @app.context_processor
    def inject_app_name():
        return {
            "app_name": app.config["APP_NAME"],
            "app_version": app.config["VERSION"],
            "now": datetime.now() 
            }
    
    return app