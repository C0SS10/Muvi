from datetime import datetime
from pymongo import ASCENDING, DESCENDING
from app.domain.models.movie import Movie
from app.domain.repositories.movie_repository import MovieRepository
from app.infrastructure.mongo_connection import database
from typing import Dict, List
from bson import ObjectId

class MongoMovieRepository(MovieRepository):
    def insert_movie(self, movie_dict: Dict) -> str:
        movie_result = database.movies.insert_one(movie_dict)
        return str(movie_result.inserted_id)
    
    def insert_many_movies(self, movies_dict: List[Dict]) -> List[str]:
        movies_identifiers = database.movies.insert_many(movies_dict)
        return [str(id) for id in movies_identifiers.inserted_ids]

    def search_movies(self, filters: Dict[str, str | None], limit: int, offset: int, sort_by: str = "title", order: str = "asc") -> List[Movie]:
        mongo_filter = {}

        if "title" in filters:
            mongo_filter["title"] = {"$regex": filters["title"], "$options": "i"}
        if "director" in filters:
            mongo_filter["director"] = {"$regex": filters["director"], "$options": "i"}
        if "year" in filters and filters["year"] is not None:
            year = int(filters["year"])
            start_date = datetime(year, 1, 1)
            end_date = datetime(year + 1, 1, 1)
            mongo_filter["release_date"] = {"$gte": start_date, "$lt": end_date}
        if "genre" in filters:
            mongo_filter["genre"] = {"$regex": filters["genre"], "$options": "i"}
        if "rating" in filters:
            mongo_filter["rating"] = filters["rating"]

        sort_direction = ASCENDING if order == "asc" else DESCENDING

        documents = (
            database.movies
            .find(mongo_filter)
            .sort(sort_by, sort_direction)
            .skip(offset)
            .limit(limit)
        )

        return [Movie.from_mongo(doc) for doc in documents]

    def count_movies(self) -> int:
        return database.movies.count_documents({})
    
    def get_movie_by_id(self, id: ObjectId) -> Movie | None:
        document = database.movies.find_one({"_id": id})
        if document:
            return Movie.from_mongo(document)
        return None
    
    def update_movie(self, id: ObjectId, movie_data: Dict) -> None:
        database.movies.update_one({"_id": id}, {"$set": movie_data})