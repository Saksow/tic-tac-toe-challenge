import json
import logging
import uuid
from typing import Dict, List

from redis import ConnectionError, StrictRedis

from storage import GameNotFound, Storage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Redis(Storage):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = self._connect()

    def _connect(self) -> StrictRedis:
        try:
            redis = StrictRedis(host=self.host, port=self.port, decode_responses=True)
            logger.info(f'Connecting to Redis Storage on {self.host}:{self.port} ...')
            redis.ping()
            logger.info('Successfully configured connection to Redis Storage')
            return redis
        except ConnectionError:
            logger.error('Could not connect to Redis Storage! Please verify its configuration')
            exit(0)

    @staticmethod
    def _key_name(pattern: str) -> str:
        return f'games:{pattern}'

    def get_all_games(self) -> List:
        all_keys = self.redis.scan_iter(match=self._key_name('*'))
        return [json.loads(game) for game in self.redis.mget(all_keys)]

    def add_game(self, obj: Dict) -> Dict:
        game_id = str(uuid.uuid4())
        obj['id'] = game_id
        key_name = self._key_name(game_id)
        self.redis.set(key_name, json.dumps(obj))
        return obj

    def set_game(self, obj: Dict) -> Dict:
        game_id = obj['id']
        key_name = self._key_name(game_id)

        if self.redis.exists(key_name) == 0:
            raise GameNotFound(f'Game ID "{game_id}" not found!')

        self.redis.set(key_name, json.dumps(obj))
        return obj

    def get_game(self, game_id: str) -> Dict:
        game = self.redis.get(self._key_name(game_id))
        if game is not None:
            return json.loads(game)
        else:
            raise GameNotFound(f'Game ID "{game_id}" not found!')
