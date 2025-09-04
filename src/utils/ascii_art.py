from pyfiglet import Figlet
from src.config import Config

class Banner:
    def __init__(self, name: str):
        self.name = name
        self.description = f"Herramienta de manejo de correos de {Config.APP_NAME}"
        self.banner = self.get_banner()
        
    def _build_title(self, name: str) -> str:
        """Genera el título en arte ASCII usando pyfiglet."""
        figlet = Figlet(font="ansi_shadow", width=80, justify="center")
        ascii_art = figlet.renderText(name)
        return ascii_art

    def get_banner(self) -> str:
        """Devuelve el banner como una cadena de texto."""
        title = self._build_title(self.name)
        banner = f'''\n{title}\n{self.description} [v{Config.VERSION}]'''
        return banner
    
    def print_banner(self) -> None:
        """Imprime el banner en la consola."""
        banner = self.banner
        print(banner)
        