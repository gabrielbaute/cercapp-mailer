import csv
import logging
from colorama import Fore, Style    
from typing import List, Dict, Optional

from src.core.mail.mailer import Mailer


class CSVProcessor:
    def __init__(self, mailer: Mailer):
        """
        Inicializa el procesador de CSV
        
        Args:
            mailer: Instancia del servicio Mailer
        """
        self.mailer = mailer
        self.module_name = "CSVProcessor"
        self.logger = logging.getLogger(f"{Fore.LIGHTMAGENTA_EX}[{self.module_name}]")
        self.logger.info(f"{self.module_name} inicializado.")
    
    def read_recipients(self, csv_file: str) -> List[Dict[str, str]]:
        """
        Lee un archivo CSV y devuelve una lista de diccionarios con los datos de cada contacto
        
        Args:
            csv_file: Ruta al archivo CSV
        Returns:
            Lista de diccionarios con los datos de cada contacto
        """
        recipients = []
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                self.logger.info(f"{Fore.LIGHTBLUE_EX}Abriendo archivo CSV: {csv_file}")
                reader = csv.DictReader(file)
                
                # Verificar columnas requeridas
                fieldnames = [f.strip() for f in reader.fieldnames] if reader.fieldnames else []
                if not all(f in fieldnames for f in ['email', 'name']):
                    self.logger.error(f"{Fore.RED}El CSV debe contener columnas 'email' y 'name'")
                    return recipients
                
                for row in reader:
                    # Limpiar datos
                    cleaned_row = {k.strip(): v.strip() if isinstance(v, str) else v 
                                 for k, v in row.items()}
                    
                    email = cleaned_row.get('email', '')
                    name = cleaned_row.get('name', '')
                    
                    # Validaciones
                    if not email:
                        self.logger.error(f"{Fore.RED}: Email vacío - Fila: {row}")
                        continue
                        
                    if not self.mailer.is_valid_email(email):
                        self.logger.error(f"{Fore.RED}: Email no válido '{email}' - Fila: {row}")
                        continue
                        
                    if not name:
                        self.logger.warning(f"{Fore.YELLOW}: Nombre vacío para email {email} - Usando valor por defecto")
                        name = "Estimado/a"
                    
                    recipients.append({'email': email, 'name': name})
                
                self.logger.info(f"{Fore.LIGHTBLUE_EX}Total de contactos válidos leídos: {len(recipients)}")
        
        except Exception as e:
            self.logger.error(f"{Fore.RED}Error leyendo el archivo CSV: {str(e)}", exc_info=True)
        
        return recipients
    

    def process_contacts(self, csv_file: str, template_name: str, subject: str) -> Dict[str, int]:
        """
        Procesa un archivo CSV y envía emails a cada contacto
        
        Args:
            csv_file: Ruta al archivo CSV
            template_name: Nombre del template a usar
            subject: Asunto del correo
            
        Returns:
            Diccionario con conteo de éxitos y fallos
        """
        result = {'success': 0, 'failures': 0}
        recipients = self.read_recipients(csv_file)
        for contact in recipients:
            email = contact['email']
            name = contact['name']
            
            if email:
                try:
                    sent = self.mailer.send_email(
                        to_email=email,
                        subject=subject,
                        template_name=template_name,
                        user_name=name,
                    )
                    
                    if sent:
                        result['success'] += 1
                    else:
                        result['failures'] += 1
                except Exception as e:
                    self.logger.error(f"{Fore.RED}Error crítico enviando email a {email}: {str(e)}", exc_info=True)
                    result['failures'] += 1
        
        
        return result