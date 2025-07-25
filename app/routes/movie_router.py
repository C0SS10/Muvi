from flask import Blueprint, redirect, request, jsonify, url_for
from werkzeug.wrappers.response import Response
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

@movie_router.route('/insert-many', methods=['POST'])
def create_movies() -> Tuple[Response, int] | Response:
        movie_service = MovieService(MongoMovieRepository())
        movies = request.get_json()

        if isinstance(movies, dict) or (isinstance(movies, list) and len(movies) == 1):
                return redirect(url_for('router.movies.create_movie'), code=307)

        response_message, status_code = movie_service.add_movies(movies)
        return jsonify({"message": response_message}), status_code