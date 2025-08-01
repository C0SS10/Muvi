from pymongo import ASCENDING
from app.domain.models.movie import Movie
from app.domain.repositories.movie_repository import MovieRepository
from app.infrastructure.mongo_connection import database
from typing import Dict, List

class MongoMovieRepository(MovieRepository):
    def insert_movie(self, movie_dict: Dict) -> str:
        movie_result = database.movies.insert_one(movie_dict)
        return str(movie_result.inserted_id)
    
    def insert_many_movies(self, movies_dict: List[Dict]) -> List[str]:
        movies_identifiers = database.movies.insert_many(movies_dict)
        return [str(id) for id in movies_identifiers.inserted_ids]

    def get_all_movies(self, limit: int, offset: int) -> List[Movie]:
        documents = database.movies.find().sort("title", ASCENDING).skip(offset).limit(limit)
        return [Movie.from_mongo(document) for document in documents]
    
    def count_movies(self) -> int:
        return database.movies.count_documents({})