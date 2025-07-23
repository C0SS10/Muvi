from typing import Dict
from abc import ABC, abstractmethod
class MovieRepository(ABC):
    @abstractmethod
    def insert_movie(self, movie_dict: Dict) -> str:
        pass