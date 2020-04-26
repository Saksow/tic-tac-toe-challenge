from abc import ABC, abstractmethod
from typing import Dict, List


class GameNotFound(Exception):
    pass


class Storage(ABC):
    """ Abstract class interfacing with a storage backend.
    """

    @abstractmethod
    def get_all_games(self) -> List:
        """ Get all saved games

        Returns:
          Games as a list
        """
        pass

    @abstractmethod
    def add_game(self, obj: Dict) -> Dict:
        """ Insert a new game

        Args:
          obj: game object as a dict
        Returns:
          Game object with a unique ID as a dict
        """
        pass

    @abstractmethod
    def set_game(self, obj: Dict) -> Dict:
        """ Update an existing game

        Args:
          obj: game object as a dict
        Returns:
          Game object as a dict
        """
        pass

    @abstractmethod
    def get_game(self, game_id: str) -> Dict:
        """ Get a game

        Args:
          game_id: game ID as a string
        Returns:
          Game object as a dict
        """
        pass
