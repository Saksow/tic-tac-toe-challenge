import os
from typing import List

from connexion import App
from flask import Flask
from flask_injector import FlaskInjector
from injector import Binder

from game.config import Config, get_config
from storage import Storage
from storage.redis import Redis


def create_app(config: Config, injected_modules: List = None) -> Flask:
    """ Create the Flask app and configure it

    Args:
      config: configuration as a Config object
      injected_modules: modules that will be injected into views as a list
    Returns:
      Configured Flask app as a Flask object
    """
    connexion_app = App('tic-tac-toe', specification_dir='api')
    connexion_app.add_api('spec.yml', validate_responses=True)

    flask_app = connexion_app.app
    flask_app.config.from_object(config)
    _inject_modules(flask_app, injected_modules)

    return flask_app


def _inject_modules(flask_app: Flask, injected_modules: List) -> None:
    """ Inject the given modules into the Flask app so that we can use them in views

    Args:
      flask_app: application as a Flask object
      injected_modules: modules that will be injected into views as a list
    """

    def _inject_redis(binder: Binder) -> None:
        binder.bind(
            Storage,
            # Here we can inject different Storage subclasses, we can also use a Storage factory
            Redis(flask_app.config['STORAGE_HOST'], flask_app.config['STORAGE_PORT']),
        )

    if injected_modules is None:
        injected_modules = [_inject_redis]

    FlaskInjector(app=flask_app, modules=injected_modules)


app = create_app(get_config(os.getenv('APP_ENV', 'development')))

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])
