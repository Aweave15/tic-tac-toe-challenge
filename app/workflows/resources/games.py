from flask_restful import Resource
from flask import (
    jsonify,
    request,
    Response,
    g
)
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from workflows.lib.models import GameBag

def get_schema():
    with open('workflows/schemas/game.schema') as f_in:
        return json.load(f_in)

class GameBagResource:
    '''
    Allow the game bag to be globally accessible as all resources will use it
    '''
    def get_game_bag(self):
        if 'game_bag' in g:
            return g.game_bag
        g.game_bag = GameBag()
        return g.game_bag


class GameHandler(Resource, GameBagResource):

    methods = ['POST', 'GET']

    def get(self, game_id):
        if self.get_game_bag().has_game(game_id):
            return jsonify(
                {
                    'game_id': game_id,
                    'game_board':self.get_game_bag().get_game_board(game_id)
                }
            )
        return Response(f'{game_id} is not an existing game', 404)

    def post(self, game_id):
        data = request.get_json()
        if self.get_game_bag().has_game(game_id):
            try:
                validate(instance=data, schema=get_schema())
            except ValidationError as validation_error:
                return Response(validation_error.message, 400)
            self.get_game_bag().update_game(game_id, data.get('game'))
            return jsonify({'status': 'Ok', 'game_id': game_id})
        else:
            return Response(f'{game_id} is not an existing game', 400)


class GameBagHandler(Resource, GameBagResource):
    methods = ['POST', 'GET']

    def get(self):
        games = [{'game_id': game.id, 'game_board': game.board} for game in self.get_game_bag().get_all_games()]
        return jsonify({
            'games': games
        })

    def post(self):
        game_id = self.get_game_bag().create_game()
        return jsonify({
            'game': game_id
        })
