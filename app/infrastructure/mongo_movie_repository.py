from app.domain.repositories.movie_repository import MovieRepository
from app.infrastructure.mongo_connection import database
from typing import Dict

class MongoMovieRepository(MovieRepository):
    def insert_movie(self, movie_dict: Dict) -> str:
        movie_result = database.movies.insert_one(movie_dict)
        return str(movie_result.inserted_id)