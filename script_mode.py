import logging
from colorama import Fore, Style

from src.server import create_script_app
from src.core import CSVProcessor, Mailer
from src.config import ConfigCercapp, ConfigSaludFinanciera
from src.cercapplogger import LoggerConfig, get_logger
from src.utils import Banner
from data import EmailSubjects

def main():
    """Función principal para ejecutar la campaña de emails"""
    LoggerConfig.setup()
    banner = Banner("Cercapp Mailer")
    
    logger = get_logger("[CercappCampañas]")

    logger.info(banner.print_banner())
    logger.info(f"{Fore.LIGHTBLUE_EX}Iniciando proceso de envío de emails en modo SCRIPT...")
    logger.warning(f"{Fore.YELLOW}En modo SCRIPT no se guardan estadísticas de envío...")
    
    try:
        # Crear aplicación y servicios
        app = create_script_app(ConfigCercapp)
        data = input(f"{Fore.YELLOW}Inserte el nombre del archivo CSV (incluya la extensión .csv): ")
        data = f"data/{data}"
        subject_input = input(f"{Fore.YELLOW}Inserte el asunto del email: ")
        
        # Importar servicios después de crear la app para evitar import circulares
        logger.info(f"{Fore.BLUE}Inicializando módulos de mail y procesamiento CSV...")
        mailer = Mailer(app)
        processor = CSVProcessor(mailer)
        
        # Ejecutar procesamiento
        result = processor.process_contacts(
            csv_file=data,
            template_name="completar_registro.html",
            subject=subject_input
        )
        
        # Mostrar resultados
        logger.info(f"{Fore.GREEN}{Style.BRIGHT}Resumen de la campaña:")
        logger.info(f"{Fore.GREEN}Emails exitosos: {result['success']}")
        logger.info(f"{Fore.RED}Fallidos: {result['failures']}")
        
        if result['failures'] == 0:
            logger.info(f"{Fore.GREEN}¡Todos los emails se enviaron correctamente!")
        else:
            logger.warning("Algunos emails no pudieron ser enviados. Revisa los logs para más detalles.")
            
    except Exception as e:
        logger.error(f"{Fore.RED}Error inesperado en la campaña: {str(e)}", exc_info=True)
    except KeyboardInterrupt:
        print("\n")
        logger.warning(f"{Fore.YELLOW}Proceso de envío de emails interrumpido por el usuario.")
    finally:
        logger.info(f"{Fore.GREEN}Cercapp Mailer finalizado.")

if __name__ == '__main__':
    main()