from flask_restful import Resource
from flask import jsonify, request, Response
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json

from workflows.lib.models import GameBag, IllegalGameMoveException

def get_game_schema():
    with open('workflows/schemas/game.schema') as f_in:
        return json.load(f_in)

def get_players_schema():
    with open('workflows/schemas/players.schema') as f_in:
        return json.load(f_in)


class GameHandler(Resource, GameBag):

    methods = ['POST', 'GET']

    def get(self, game_id):
        game = self.get_game(game_id)
        if game:
            return jsonify(
                {
                    'game_id': game.get_id(),
                    'game_board':game.get_board()
                }
            )
        return Response(f'{game_id} is not an existing game', 404)

    def post(self, game_id):
        data = request.get_json()
        if self.has_game(game_id):
            try:
                validate(instance=data, schema=get_game_schema())
            except ValidationError as validation_error:
                return Response(validation_error.message, 400)

            # update game
            try:
                updated_game = self.update_game(game_id, data.get('game_board'))
                return jsonify({'status': 'Updated', 'game_id': updated_game.get_id(), 'game_board': updated_game.get_board()})
            except IllegalGameMoveException as illegal_game_move_exception:
                return Response(illegal_game_move_exception.args, 400)
        else:
            return Response(f'{game_id} is not an existing game', 400)


class GameBagHandler(Resource, GameBag):
    methods = ['POST', 'GET']

    def get(self):
        games = self.get_games()
        filtered = [{'game_id': g.get_id(), 'game_board': g.get_board()} for g in games]
        return jsonify({
            'games': filtered
        })

    def post(self):
        data = request.get_json()
        try:
            validate(instance=data, schema=get_players_schema())
        except ValidationError as validation_error:
            return Response(validation_error.message, 400)
        game = self.create_game(data.get('players'))
        return jsonify({
            'game_id': game.get_id(),
            'players': game.get_players()
        })
