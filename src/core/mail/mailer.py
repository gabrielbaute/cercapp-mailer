from flask import Flask, render_template_string
from flask_mail import Mail, Message
from typing import Optional, Dict, Any
from colorama import Fore, Style
import logging
import re

class Mailer:
    def __init__(self, app: Flask):
        """
        Inicializa el servicio de correo
        
        Args:
            app: Instancia de Flask
        """
        self.app = app
        self.mail = Mail(app)
        self.module_name = "CercappMailer"
        self.logger = logging.getLogger(f"{Fore.LIGHTGREEN_EX}[{self.module_name}]")
        self.logger.info(f"{self.module_name} inicializado.")

    def build_subject(self, user_name: str, subject_text: str) -> str:
        """
        Construye el asunto del email
        
        Args:
            user_name: Nombre del usuario para personalizar el asunto
            subject_text: Texto del asunto específico

        Returns:
            Asunto del email
        """
        subject_text = subject_text if subject_text else "Notificación de Cercapp"
        return f"✨ {user_name}, {subject_text}"

    def is_valid_email(self, email: str) -> bool:
        """
        Validación básica de formato de email

        Args:
            email: Dirección de correo a validar

        Returns:
            True si el email es válido, False si no lo es        
        """
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    def load_template(self, template_name: str, **context: Dict[str, Any]) -> Optional[str]:
        """
        Carga una plantilla de email con los partials incluidos
        
        Args:
            template_name: Nombre del template en la carpeta emails/
            context: Variables para renderizar el template
            
        Returns:
            Contenido HTML renderizado o None si hay error
        """
        try:
            self.logger.debug(f"Cargando plantilla {template_name} con contexto: {context}")
            
            # Asegurar que tenemos contexto de aplicación
            with self.app.app_context():
                return render_template_string(
                    f"{{% include 'emails/{template_name}' %}}",
                    **context
                )
        except Exception as e:
            self.logger.error(f"{Fore.RED}Error cargando plantilla {template_name}: {str(e)}", exc_info=True)
            return None

    def send_email(self, to_email: str, template_name: str, subject: Optional[str] = None, **template_vars: Dict[str, Any]) -> bool:
        """
        Envía un email usando una plantilla
        
        Args:
            to_email: Dirección de correo destino
            subject: Asunto del correo
            template_name: Nombre del template a usar
            template_vars: Variables para el template
            
        Returns:
            True si el envío fue exitoso, False si falló
        """
        try:
            # Renderizar el template dentro del contexto
            with self.app.app_context():
                html_content = self.load_template(template_name, **template_vars)
                
                if not html_content:
                    self.logger.error(f"{Fore.RED}No se pudo generar el contenido para {to_email}")
                    return False
                    
                self.logger.info(f"Enviando email a {to_email}")
                
                msg = Message(
                    subject=self.build_subject(
                        user_name=template_vars.get('user_name', 'Usuario'),
                        subject_text=subject),
                    recipients=[to_email],
                    html=html_content,
                    sender=self.app.config['MAIL_DEFAULT_SENDER'],
                    #bcc=self.app.config.get('MAIL_BCC', []),
                )
                self.mail.send(msg)
                
            self.logger.debug(f"Email enviado exitosamente a {to_email}")
            return True
        except Exception as e:
            self.logger.error(f"{Fore.RED}Error enviando email a {to_email}: {str(e)}", exc_info=True)
            return False