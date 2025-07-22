from app.infrastructure.mongo_connection import database
from typing import Dict

"""
    Insert a movie into the MongoDB database.
    
    :param movie_dict: The movie data to insert.
    :return: The ID of the inserted movie.
"""
def insert_movie(movie_dict: Dict) -> str:
    movie_result = database.movies.insert_one(movie_dict)
    return str(movie_result.inserted_id)