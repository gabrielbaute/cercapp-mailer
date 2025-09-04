from typing import Optional, Dict, Any
from src.core import Mailer, CSVProcessor

class MailerController:
    def __init__(self, mailer: Mailer, csv_processor: CSVProcessor):
        self.mailer = mailer
        self.csv_processor = csv_processor
        self.controller_name = "MailerController"

    def send_emails_from_csv(
            self, 
            csv_file_path: str, 
            subject: str, 
            template_name: str, 
            **template_vars: Optional[Dict[str, Any]]):
        """Envía correos a una lista de destinatarios desde un archivo CSV"""
        recipients = self.csv_processor.read_recipients(csv_file_path)
        for recipient in recipients:
            self.mailer.send_email(recipient, subject, template_name, **template_vars)