from flask_restful import Resource
from flask import (
    jsonify,
    g,
    request,
    Response
)
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def get_schema():
    with open('workflows/schemas/game.schema') as f_in:
        return json.load(f_in)


class GameHandler(Resource):

    methods = ['POST', 'GET']

    def get(self, game_id):
        if g.game_bag.has_game(game_id):
            return jsonify(
                {
                    'game_id': game_id,
                    'game_board': g.game_bag.get_game_board(game_id)
                }
            )
        return Response(f'{game_id} is not an existing game', 404)

    def post(self, game_id):
        data = request.get_json()
        if g.game_bag.has_game(game_id):
            try:
                validate(instance=data, schema=get_schema())
            except ValidationError as ve:
                return Response(ve.message, 400)
            g.game_bag.update_game(game_id, data.get('game'))
            return jsonify({'status': 'Ok', 'game_id': game_id})
        else:
            return Response(f'{game_id} is not an existing game', 400)


class GameBagHandler(Resource):
    methods = ['POST', 'GET']

    def get(self):
        games = [{'game_id': game.id, 'game_board': game.board} for game in g.game_bag.get_all_games()]
        return jsonify({
            'games': games
        })

    def post(self):
        game_id = g.game_bag.create_game()
        return jsonify({
            'game': game_id
        })
