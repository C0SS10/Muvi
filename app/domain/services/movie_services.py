from app.domain.models.movie import Movie
from typing import Tuple, Dict
from pydantic import ValidationError
from app.domain.repositories.movie_repositories import insert_movie


def add_movie(movie: Dict) -> Tuple[str, int]:
    try:
        movie_validated = Movie(**movie)
        movie_dict = movie_validated.model_dump(exclude={"id"})
        movie_id = insert_movie(movie_dict)

        return f"Movie created with ID: {movie_id}", 201
    except ValidationError as error:
        message = error.errors()[0].get("msg", "Invalid data")

        return message, 422