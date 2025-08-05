from app.domain.models.movie import Movie
from typing import List, Tuple, Dict
from bson import ObjectId
from pydantic import ValidationError
from app.domain.repositories.movie_repository import MovieRepository

class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self._repository = movie_repository

    def add_movie(self, movie: Dict) -> Tuple[str, int]:
        try:
            movie_validated = Movie(**movie)
            movie_dict = movie_validated.model_dump(exclude={"id"})
            movie_id = self._repository.insert_movie(movie_dict)

            return f"Movie created with ID: {movie_id}", 201
        except ValidationError as error:
            message = error.errors()[0].get("msg", "Invalid data")

            return message, 422
        
    def add_many_movies(self, movies: List[Dict]) -> Tuple[str, int]:
        try:
            movies_validated = [Movie(**movie) for movie in movies]
            movies_dict = [movie.model_dump(exclude={"id"}) for movie in movies_validated]
            movies_ids = self._repository.insert_many_movies(movies_dict)

            return f"Movies created with IDs: {', '.join(movies_ids)}", 201
        except ValidationError as error:
            message = error.errors()[0].get("msg", "Invalid data")

            return message, 422
    
    def get_movies(self, filters: Dict[str, str | None], limit: int , offset: int) -> List[Movie]:
        total_movies = self._repository.count_movies()
        if limit <= 0 or offset < 0 or offset >= total_movies:
            raise ValueError("Invalid pagination parameters")

        return self._repository.search_movies(filters=filters, limit=limit, offset=offset)

    def get_movie_by_id(self, id: ObjectId) -> Movie | None:
        return self._repository.get_movie_by_id(id)