from src.database import db
from src.controllers.user_controller import UsersController
from src.controllers.mailer_controller import MailerController

class ControllerFactory:
    """Controller Factory"""

    def __init__(self, db_instance=db, current_user=None):
        if not hasattr(db_instance, "session"):
            raise ValueError("El objeto db no parece ser una instancia válida de SQLAlchemy")
        
        self.db = db_instance
        self.current_user = current_user
    
    def get_controller(self, controller_name):
        """Retorna una instancia del controlador solicitado."""
        if controller_name == "users":
            return UsersController(self.db, self.current_user)
        if controller_name == "mailer":
            return MailerController()
        raise ValueError(f"Controlador no soportado: {controller_name}")
        return None