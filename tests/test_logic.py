import pytest

from game.logic import InvalidMove, _check_player_won, init_game, make_move


def test_init_game():
    players = [{'name': 'Mario'}, {'name': 'Luigi'}]
    game = init_game(players)

    expected_parts = {
        'status': 'in_progress',
        'winning_player_number': None,
        'next_player_number': 1,
        'moves': []
    }
    assert all(i in game.items() for i in expected_parts.items())

    game_players = game['players']
    assert len(game_players) == 2

    assert game_players[0]['name'] != game_players[1]['name']
    assert game_players[0]['name'] in {'Mario', 'Luigi'}

    assert game_players[0]['number'] != game_players[1]['number']
    assert game_players[0]['number'] in {1, 2}

    assert game_players[0]['sign'] != game_players[1]['sign']
    assert game_players[0]['sign'] in {'X', 'O'}


def test_make_move_fail_game_is_done():
    game = {'id': 'foo-bar', 'status': 'done'}

    with pytest.raises(InvalidMove) as e:
        make_move(game, {})

    assert str(e.value) == (f'Game ID ({game["id"]}) is not in progress anymore, '
                            f'current status is ({game["status"]})!')


def test_make_move_fail_wrong_player():
    game = {'status': 'in_progress', 'next_player_number': 1}
    move = {'player_number': 2}

    with pytest.raises(InvalidMove) as e:
        make_move(game, move)

    assert str(e.value) == (f'Expecting player number ({game["next_player_number"]}) to make a '
                            f'move but found player number ({move["player_number"]}) instead!')


def test_make_move_fail_tile_used_before():
    game = {'status': 'in_progress', 'next_player_number': 1,
            'moves': [{'player_number': 1, 'tile_number': 5},
                      {'player_number': 2, 'tile_number': 3}]}
    move = {'player_number': 1, 'tile_number': 5}

    with pytest.raises(InvalidMove) as e:
        make_move(game, move)

    assert str(e.value) == f'Tile number ({move["tile_number"]}) was already played!'


def test_make_move_success_inserted():
    game = {'status': 'in_progress', 'next_player_number': 1,
            'moves': [{'player_number': 1, 'tile_number': 5},
                      {'player_number': 2, 'tile_number': 3}]}
    move = {'player_number': 1, 'tile_number': 6}

    game = make_move(game, move)

    assert game['last_update_time'] == move['create_time']
    assert len(game['moves']) == 3
    assert move in game['moves']
    assert game['next_player_number'] == 2


def test_check_player_won_horizontal():
    game = {'status': 'in_progress',
            'moves': [
                {'player_number': 1, 'tile_number': 6},
                {'player_number': 2, 'tile_number': 3},
                {'player_number': 1, 'tile_number': 4},
                {'player_number': 2, 'tile_number': 2},
                {'player_number': 1, 'tile_number': 5},  # Last move
            ]}
    move = {'player_number': 1, 'tile_number': 5}

    game = _check_player_won(game, move)

    assert game['winning_player_number'] == 1
    assert game['next_player_number'] is None
    assert game['status'] == 'done'


def test_check_player_won_vertical():
    game = {'status': 'in_progress',
            'moves': [
                {'player_number': 1, 'tile_number': 5},
                {'player_number': 2, 'tile_number': 3},
                {'player_number': 1, 'tile_number': 8},
                {'player_number': 2, 'tile_number': 1},
                {'player_number': 1, 'tile_number': 2},  # Last move
            ]}
    move = {'player_number': 1, 'tile_number': 2}

    game = _check_player_won(game, move)

    assert game['winning_player_number'] == 1
    assert game['next_player_number'] is None
    assert game['status'] == 'done'


def test_check_player_won_diagonal():
    game = {'status': 'in_progress',
            'moves': [
                {'player_number': 1, 'tile_number': 5},
                {'player_number': 2, 'tile_number': 2},
                {'player_number': 1, 'tile_number': 1},
                {'player_number': 2, 'tile_number': 7},
                {'player_number': 1, 'tile_number': 9},  # Last move
            ]}
    move = {'player_number': 1, 'tile_number': 9}

    game = _check_player_won(game, move)

    assert game['winning_player_number'] == 1
    assert game['next_player_number'] is None
    assert game['status'] == 'done'


def test_check_player_did_not_win():
    game = {'status': 'in_progress',
            'moves': [
                {'player_number': 1, 'tile_number': 6},
                {'player_number': 2, 'tile_number': 5},
                {'player_number': 1, 'tile_number': 9},
                {'player_number': 2, 'tile_number': 3},
                {'player_number': 1, 'tile_number': 7},  # Last move
            ]}
    move = {'player_number': 1, 'tile_number': 7}

    game = _check_player_won(game, move)

    assert game['status'] == 'in_progress'
