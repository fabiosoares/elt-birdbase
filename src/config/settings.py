import os
import sys
import inspect


def factory(env):

    classes_tuple = inspect.getmembers(sys.modules[__name__], inspect.isclass)

    for current_class in classes_tuple:
        if env == current_class[1].ENV:
            return current_class[1]
    return ProdConfig


class Config(object):
    """Base configuration."""

    CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(
        os.path.join(CONFIG_DIR, os.pardir, os.pardir, os.pardir)
    )
    ENV = "base"

    GCP = {
        "PROJECT": "projetoomni",
        "REGION": "us-central1",
        "KEY_PATH": PROJECT_ROOT + "/support/keys/ammo-varejo-etl.json",
    }


class ProdConfig(Config):
    """Production configuration."""

    ENV = "prod"


class DevelopmentConfig(Config):
    """Development configuration."""

    ENV = "development"
