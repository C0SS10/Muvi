from typing import Dict, List
from abc import ABC, abstractmethod

from app.domain.models.movie import Movie


class MovieRepository(ABC):
    @abstractmethod
    def insert_movie(self, movie_dict: Dict) -> str:
        pass

    @abstractmethod
    def insert_many_movies(self, movies_dict: List[Dict]) -> List[str]:
        pass

    @abstractmethod
    def get_all_movies(self) -> List[Movie]:
        pass