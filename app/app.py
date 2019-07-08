from flask_restful import Api
from flask import Flask
from flask import g
from workflows.resources.health import HealthHandler
from workflows.resources.games import GameHandler, GameBagHandler
from workflows.lib.models import GameBag

APP_NAME = 'tac-tac-toe'

app = Flask(APP_NAME)

api = Api(app)

# since gamebag is needed globally, set as prehook, if application builds probably move to Resource level
@app.before_request
def pre_hook():
    g.game_bag = GameBag()


api.add_resource(HealthHandler, '/healthcheck/')
api.add_resource(GameHandler, '/api/games/<game_id>')
api.add_resource(GameBagHandler, '/api/games/')

if __name__ == '__main__':
    # for dev purposes, use WSGI server for non-dev server
    app.run(debug=True, host='0.0.0.0')
