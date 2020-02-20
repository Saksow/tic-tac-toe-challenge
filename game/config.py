import os
from logging import getLogger


class Config:
    HOST = os.getenv('APP_HOST', 'localhost')
    PORT = int(os.getenv('APP_PORT', '5000'))
    STORAGE_HOST = os.getenv('APP_STORAGE_HOST', 'localhost')
    STORAGE_PORT = int(os.getenv('APP_STORAGE_PORT', '6379'))


class Development(Config):
    ENV = 'development'


class Production(Config):
    ENV = 'production'


def get_config(app_env: str) -> Config:
    logger = getLogger(__name__)
    config = {
        'development': Development(),
        'production': Production(),
        'default': Development(),
    }
    try:
        return config[app_env]
    except KeyError:
        # Added safety for when APP_ENV was set to a non-existent config name
        logger.warning(f'Env "{app_env}" does not exist! Falling back to default config')
        return config['default']
