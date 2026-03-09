from dotenv import load_dotenv

from src.config.app_factory import AppFactory

load_dotenv()
app = AppFactory.factory()
logging = app.logger


def import_modules():
    from src.controllers import names_controller


import_modules()
