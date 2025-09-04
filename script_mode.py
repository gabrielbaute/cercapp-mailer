import logging

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
    logger.info("Iniciando proceso de envío de emails...")
    
    try:
        # Crear aplicación y servicios
        app = create_script_app(ConfigCercapp)
        
        # Importar servicios después de crear la app para evitar import circulares
        logger.info("Inicializando módulos de mail y procesamiento CSV...")
        mailer = Mailer(app)
        processor = CSVProcessor(mailer)
        
        # Ejecutar procesamiento
        result = processor.process_contacts(
            csv_file=app.config["PRUEBA"],
            template_name="incentivar.html",
            subject=EmailSubjects.INCENTIVAR
        )
        
        # Mostrar resultados
        logger.info(f"Resumen de la campaña:")
        logger.info(f"Emails exitosos: {result['success']}")
        logger.info(f"Fallidos: {result['failures']}")
        
        if result['failures'] == 0:
            logger.info("¡Todos los emails se enviaron correctamente!")
        else:
            logger.warning("Algunos emails no pudieron ser enviados. Revisa los logs para más detalles.")
            
    except Exception as e:
        logger.error(f"Error inesperado en la campaña: {str(e)}", exc_info=True)
    finally:
        logger.info("Proceso de envío de emails completado.")

if __name__ == '__main__':
    main()