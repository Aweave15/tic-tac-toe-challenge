import os

from flask_restful import Api
from flask import Flask
from flask import g

from workflows.resources.health import HealthHandler
from workflows.resources.games import GameHandler, GameBagHandler
from workflows.lib.models import GameBag



def create_app(testing=False):
    app = Flask(os.environ.get('APP_NAME'))
    app.testing = testing
    api = Api(app)

    api.add_resource(HealthHandler, '/healthcheck/')
    api.add_resource(GameHandler, '/api/games/<game_id>')
    api.add_resource(GameBagHandler, '/api/games/')

    return app