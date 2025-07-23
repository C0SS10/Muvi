from flask import Blueprint, request, Response, jsonify
from typing import Tuple
from app.domain.services.movie_services import MovieService
from app.infrastructure.mongo_movie_repository import MongoMovieRepository

movie_router = Blueprint('movies', __name__)

@movie_router.route('/', methods=['POST'])
def create_movie() -> Tuple[Response, int]:
        movie_service = MovieService(MongoMovieRepository())
        movie = request.get_json()
        response_message, status_code = movie_service.add_movie(movie)
        return jsonify({"message": response_message}), status_code