from typing import Dict, List, Tuple

from injector import inject

from game import logic
from storage import GameNotFound, Storage


@inject
def get_games(store: Storage) -> Tuple[Dict[str, List], int]:
    return {'games': store.get_all_games()}, 200


@inject
def create_game(store: Storage, body) -> Tuple[Dict, int]:
    new_game = logic.init_game(body['players'])
    return store.add_game(new_game), 201


@inject
def get_game(store: Storage, game_id: str) -> Tuple[Dict, int]:
    try:
        return store.get_game(game_id), 200
    except GameNotFound as e:
        return _http_error(404, str(e))


@inject
def create_move(store: Storage, game_id: str, body) -> Tuple[Dict, int]:
    try:
        game = store.get_game(game_id)
        game = logic.make_move(game, body)
        return store.set_game(game), 201
    except logic.InvalidMove as e:
        return _http_error(400, str(e))
    except GameNotFound as e:
        return _http_error(404, str(e))


def _http_error(code: int, detail: str) -> Tuple[Dict, int]:
    http_codes = {
        400: 'Bad Request',
        404: 'Not Found',
    }
    return {
               'detail': detail,
               'status': code,
               'title': http_codes[code],
           }, code
