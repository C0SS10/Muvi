from datetime import datetime
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

    def search_movies(self, filters: Dict[str, str | None], limit: int, offset: int) -> List[Movie]:
        mongo_filter = {}

        if "title" in filters:
            mongo_filter["title"] = {"$regex": filters["title"], "$options": "i"}
        if "director" in filters:
            mongo_filter["director"] = {"$regex": filters["director"], "$options": "i"}
        if "year" in filters and filters["year"] is not None:
            try:
                year = int(filters["year"])
                start_date = datetime(year, 1, 1)
                end_date = datetime(year + 1, 1, 1)
                mongo_filter["release_date"] = {"$gte": start_date, "$lt": end_date}
            except ValueError:
                raise ValueError("Year must be an integer")
        if "genre" in filters:
            mongo_filter["genre"] = {"$regex": filters["genre"], "$options": "i"}
        if "rating" in filters:
            mongo_filter["rating"] = filters["rating"]

        documents = (
            database.movies
            .find(mongo_filter)
            .sort("title", ASCENDING)
            .skip(offset)
            .limit(limit)
        )

        return [Movie.from_mongo(doc) for doc in documents]

    def count_movies(self) -> int:
        return database.movies.count_documents({})