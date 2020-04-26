import random
from datetime import datetime, timezone
from typing import Dict, List

PLAYERS_CONF = {
    1: 'X',
    2: 'O'
}

WIN_COMBINATIONS = {
    frozenset({1, 2, 3}),
    frozenset({4, 5, 6}),
    frozenset({7, 8, 9}),
    frozenset({1, 4, 7}),
    frozenset({2, 5, 8}),
    frozenset({3, 6, 9}),
    frozenset({1, 5, 9}),
    frozenset({3, 5, 7}),
}


class InvalidMove(Exception):
    pass


def init_game(players: List[Dict]) -> Dict:
    current_time = _get_current_time_utc()
    game = {
        'players': _randomly_assign_players(players),
        'create_time': current_time,
        'last_update_time': current_time,
        'status': 'in_progress',
        'winning_player_number': None,
        'next_player_number': 1,  # Player who gets assigned the number 1 will always start
        'moves': []
    }
    return game


def make_move(game: Dict, move: Dict) -> Dict:
    _validate_move(game, move)
    game = _insert_move(game, move)
    return _check_player_won(game, move)


def _validate_move(game: Dict, move: Dict) -> None:
    if game['status'] != 'in_progress':
        raise InvalidMove(f'Game ID ({game["id"]}) is not in progress anymore, current status is '
                          f'({game["status"]})!')

    if game['next_player_number'] != move['player_number']:
        raise InvalidMove(f'Expecting player number ({game["next_player_number"]}) to make a move '
                          f'but found player number ({move["player_number"]}) instead!')

    if move['tile_number'] in [m['tile_number'] for m in game['moves']]:
        raise InvalidMove(f'Tile number ({move["tile_number"]}) was already played!')


def _insert_move(game: Dict, move: Dict) -> Dict:
    current_time = _get_current_time_utc()
    game['last_update_time'] = current_time
    move['create_time'] = current_time
    game['moves'].append(move)
    game['next_player_number'] = 1 if move['player_number'] == 2 else 2
    return game


def _check_player_won(game: Dict, move: Dict) -> Dict:
    # Only the latest move could have won the game, we just need to check if the player now
    # controls enough tiles. We could write a more complex logic which can check at any time if
    # any player won the game, but this simple solution should be enough for the current problem.
    possible_win_combinations = {c for c in WIN_COMBINATIONS if move['tile_number'] in c}
    player_tiles = {m['tile_number'] for m in game['moves'] if
                    m['player_number'] == move['player_number']}

    has_won = False
    for win_combination in possible_win_combinations:
        if win_combination.issubset(player_tiles):
            has_won = True
            break

    if has_won:
        game['winning_player_number'] = move['player_number']
        game['next_player_number'] = None
        game['status'] = 'done'

    return game


def _randomly_assign_players(players: List[Dict]) -> List[Dict]:
    player_numbers = list(PLAYERS_CONF.keys())
    random.shuffle(player_numbers)

    for i, player in enumerate(players):
        player.update(number=player_numbers[i], sign=PLAYERS_CONF[player_numbers[i]])

    return players


def _get_current_time_utc() -> str:
    return datetime.now(timezone.utc).isoformat()
