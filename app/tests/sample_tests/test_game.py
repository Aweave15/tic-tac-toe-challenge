from workflows.lib.models import Game
import json


'''
Basic test case to know if we construct a new game correctly from players
'''
def test_new_game():
    players = ['player1', 'player2']
    g = Game(players=players)
    for i in range(3):
        for x in range(3):
            assert not g.get_board()[i][x]

    assert set(g.get_next_up()) == set(players)

    assert g.get_piece(players[0]) in 'XO'
    assert g.get_piece(players[1]) in 'XO'
    assert g.get_piece(players[0]) != g.get_piece(players[1])

    assert g.get_player('X')
    assert g.get_player('O')
    assert g.get_player('X') != g.get_player('O')

    assert g.get_id() and len(g.get_id()) > 0


board = [
    ['X', None, None],
    [None, None, None],
    [None, None, None]
]
game_raw = {
    'game_id': 'test_game_id',
    'players': [
        {'player': 'player1',
        'piece': 'X'},
        {'player': 'player2',
        'piece': 'O'}
    ],
    'board': board,
    'last_played_by': 'player1'
}


'''
Basic test case to know if we construct a game correctly from string
'''
def test_load_game():
    json_str = json.dumps(game_raw)
    g = Game(game_str=json_str)
    assert g.get_id() == 'test_game_id'

    assert g.get_last_played_by() == 'player1'
    assert len(g.get_next_up()) == 1 and g.get_next_up()[0] == 'player2'
    assert g.get_board() == board

    assert g.get_piece('player1') == 'X'
    assert g.get_piece('player2') == 'O'

    assert g.get_player('X') == 'player1'
    assert g.get_player('O') == 'player2'
