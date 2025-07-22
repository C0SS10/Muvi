from flask import Blueprint, request, Response, jsonify
from typing import Tuple

from app.domain.services.movie_services import add_movie

movie_router = Blueprint('movies', __name__)

@movie_router.route('/', methods=['POST'])
def create_movie() -> Tuple[str, int] | Tuple[Response, int]:
    movie = request.get_json()
    message, status_code = add_movie(movie)

    return jsonify({"message": message}), status_code
