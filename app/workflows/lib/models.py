from redis import Redis
import uuid
import ast
from collections import namedtuple
from core import settings
import json

PIECES = 'XO'


class IllegalGameMoveException(Exception):
    pass


GameChange = namedtuple('GameChange', ['old_move', 'new_move'])


'''
GameBag acts as an abstraction over the backend redis cache
'''
class GameBag:

    def __init__(self):
        self.redis_cache = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, encoding="utf-8", decode_responses=True)

    def get_game_ids(self):
        return self.redis_cache.keys()

    def get_games(self):
        return [Game(self.redis_cache.get(g)) for g in self.get_game_ids()] 

    def has_game(self, game_id):
        return self.redis_cache.exists(game_id)

    def get_game(self, game_id):
        if self.has_game(game_id):
            return Game(game_str=self.redis_cache.get(game_id))
        return None

    def create_game(self, players):
        game = Game(players=players)
        self.redis_cache.set(game.get_id(), str(game))
        return game

    def update_game(self, game_id, game_board):
        game = self.get_game(game_id)
        if not game:
            raise Exception('Can not update a game that does not exist on server')
        old_board = game.get_board()
        
        # get all changes on the board
        changes = []
        for i in range(3):
            for x in range(3):
                original = old_board[i][x]
                updated = game_board[i][x]
                if old_board[i][x] != game_board[i][x]:
                    changes.append(GameChange(original, updated))

        # check that a change was made
        if len(changes) == 0:
            raise IllegalGameMoveException('Invalid request, must change at least 1 position on the board')

        # check that there was only one change
        if len(changes) > 1:
            raise IllegalGameMoveException('Invalid request, can only place 1 position on board at a time')

        # check to make sure single change was not overwriting an existing position
        if changes[0].old_move:
            raise IllegalGameMoveException('Can not overwrite a position, must make move on null spaces on board')

        # check to make sure it's the correct players turn
        if game.get_player(changes[0].new_move) not in game.get_next_up():
            raise IllegalGameMoveException(f"It is not your turn, it is {game.get_next_up()[0]}'s turn")

        # edge cases are checked, can safely update board
        game.update_board(game_board, game.get_player(changes[0].new_move))
        self.redis_cache.set(game_id, str(game))
        return game

'''
Game is just an abstraction over our internal python dict/json
'''
class Game:

    def __init__(self, game_str=None, players=None):

        if game_str and players:
            raise Exception('Illegal args, must pass in players (new game) or existing game_str')

        if game_str:
            self.game = json.loads(game_str)

        elif players:
            new_game = {}
            new_game['board'] = [[None] * 3] * 3
            new_game['players'] = []
            # assign player a piece (X or O) based on index - doesn't matter
            for i in range(2):
                new_game['players'].append({'player': players[i], 'piece': PIECES[i]})
            new_game['last_played_by'] = None
            new_game['game_id'] = uuid.uuid4().hex
            self.game = new_game

    def get_game(self):
        return self.game

    def get_players(self):
        return self.game.get('players')

    def get_last_played_by(self):
        return self.game.get('last_played_by')

    def get_id(self):
        return self.game.get('game_id')

    def get_board(self):
        return self.game.get('board')

    # json schema dictates exactly 2 players, can afford O(n=2) lookups
    def get_piece(self, player):
        players = self.get_players()
        for p in players:
            if p.get('player') == player:
                return p.get('piece')
        return None

    def get_player(self, piece):
        players = self.get_players()
        for p in players:
            if p.get('piece') == piece:
                return p.get('player')
        return None

    def get_next_up(self):
        players = self.get_players()
        return [p.get('player') for p in players if p.get('player') != self.get_last_played_by()]

    def update_board(self, board, player):
        self.game['board'] = board
        self.game['last_played_by'] = player

    def __str__(self):
        return json.dumps(self.game)
