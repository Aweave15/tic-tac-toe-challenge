from redis import Redis
import uuid
import ast
from collections import namedtuple
import os


Game = namedtuple('Game', ['id', 'board'])


class GameBag:

    def __init__(self):
        self.redis_cache = Redis(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'), charset="utf-8", decode_responses=True)

    def get_game_ids(self):
        return self.redis_cache.keys()

    def get_all_games(self):
        games = []
        for game_id in self.get_game_ids():
            games.append(Game(game_id, self.get_game_board(game_id)))
        return games

    def has_game(self, game_id):
        return self.redis_cache.exists(game_id)

    def get_game_board(self, game_id):
        game = GameBoard(self.redis_cache.get(game_id))
        return game.board

    def create_game(self):
        game_id = uuid.uuid4().hex
        while self.has_game(game_id):
            game_id = uuid.uuid4().hex
        self.redis_cache.set(game_id, str(GameBoard().board))
        return game_id

    #TODO add more validation on game update ie. correct player making move, only 1 move, etc.
    def update_game(self, game_id, game_board):
        self.redis_cache.set(game_id, str(game_board))


class GameBoard:

    def __init__(self, board=None):
        if board:
            if isinstance(board, list):
                self.board = board
            elif isinstance(board, str):
                self.board = ast.literal_eval(board)
        else:
            self.board = [[None] * 3] * 3

    def get_board(self):
        return self.board
