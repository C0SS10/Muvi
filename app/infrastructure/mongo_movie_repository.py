from app.domain.repositories.movie_repository import MovieRepository
from app.infrastructure.mongo_connection import database
from typing import Dict, List

class MongoMovieRepository(MovieRepository):
    def insert_movie(self, movie_dict: Dict) -> str:
        movie_result = database.movies.insert_one(movie_dict)
        return str(movie_result.inserted_id)
    
    def insert_movies(self, movies_dict: List[Dict]) -> List[str]:
        movies_identifiers = database.movies.insert_many(movies_dict)
        return [str(id) for id in movies_identifiers.inserted_ids]