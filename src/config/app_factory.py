"""
The app module, containing the app factory function.
https://github.com/gothinkster/flask-realworld-example-app/blob/master/conduit/app.py
"""

import os

import src.config.settings as settings
from flask import Flask
from flask.logging import default_handler


class AppFactory:
    app = Flask("elt-birdbase")

    @staticmethod
    def factory():
        config_object = settings.factory(os.environ.get("FLASK_ENV"))

        AppFactory.app.url_map.strict_slashes = False
        AppFactory.app.config.from_object(config_object)
        AppFactory.app.args = {}

        AppFactory.register_logger()

        return AppFactory.app

    @staticmethod
    def register_logger():
        AppFactory.app.logger.addHandler(default_handler)
