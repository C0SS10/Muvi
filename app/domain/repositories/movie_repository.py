from typing import Dict, List
from abc import ABC, abstractmethod


class MovieRepository(ABC):
    @abstractmethod
    def insert_movie(self, movie_dict: Dict) -> str:
        pass

    @abstractmethod
    def insert_many_movies(self, movies_dict: List[Dict]) -> List[str]:
        pass