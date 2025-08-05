from typing import Dict, List
from abc import ABC, abstractmethod

from bson import ObjectId

from app.domain.models.movie import Movie


class MovieRepository(ABC):
    @abstractmethod
    def insert_movie(self, movie_dict: Dict) -> str:
        pass

    @abstractmethod
    def insert_many_movies(self, movies_dict: List[Dict]) -> List[str]:
        pass

    @abstractmethod
    def search_movies(self, filters: Dict[str, str | None], limit: int, offset: int) -> List[Movie]:
        pass

    @abstractmethod
    def count_movies(self) -> int:
        pass

    @abstractmethod
    def get_movie_by_id(self, id: ObjectId) -> Movie | None:
        pass