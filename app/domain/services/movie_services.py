from app.domain.models.movie import Movie
from typing import Tuple, Dict
from app.domain.repositories.movie_repositories import insert_movie


def add_movie(movie: Dict) -> Tuple[str, int]:
    movie_validated = Movie(**movie)
    movie_dict = movie_validated.model_dump(exclude={"id"})

    movie_id = insert_movie(movie_dict)

    return f"Movie created with ID: {movie_id}", 201