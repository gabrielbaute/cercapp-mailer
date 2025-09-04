from src import create_app
from src.config import Config
from src.cercapplogger import LoggerConfig

app = create_app()
logging = LoggerConfig()

if __name__ == "__main__":
    logging.setup()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)