from core import settings

from flask_restful import Api
from flask import Flask

from workflows.resources.health import HealthHandler
from workflows.resources.games import GameHandler, GameBagHandler


def create_app(testing=False):
    app = Flask(settings.APP_NAME)
    app.testing = testing
    api = Api(app)

    api.add_resource(HealthHandler, '/healthcheck/')
    api.add_resource(GameHandler, '/api/games/<game_id>')
    api.add_resource(GameBagHandler, '/api/games/')

    return app
