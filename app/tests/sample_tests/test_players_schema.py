import json


''''
Test cases to check that player payloads are being validated correctly on game creation request
'''

def test_no_players(client):
    data = {}
    response = client.post('api/games/', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400


def test_one_player(client):
    data = {
        'players': ['player1']
    }
    response = client.post('api/games/', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400

def test_one_player(client):
    data = {
        'players': ['player1', 'player2', 'player3']
    }
    response = client.post('api/games/', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400


def test_int_player(client):
    data = {
        'players': ['player1', 2]
    }
    response = client.post('api/games/', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400


def test_same_players(client):
    data = {
        'players': ['player1', 'player1']
    }
    response = client.post('api/games/', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400


def test_valid_players(client):
    data = {
        'players': ['player1', 'player2']
    }
    response = client.post('api/games/', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200