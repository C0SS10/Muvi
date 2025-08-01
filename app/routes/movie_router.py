from flask import Blueprint, redirect, request, jsonify, url_for
from werkzeug.wrappers.response import Response
from typing import Tuple
from app.domain.models.movie import Movie
from app.domain.services.movie_services import MovieService
from app.infrastructure.mongo_movie_repository import MongoMovieRepository

INTERNAL_SERVER_ERROR_MSG = "Internal server error"
PAGINATION_ERROR_MSG = "Invalid pagination parameters"

movie_router = Blueprint('movies', __name__)

@movie_router.route('', methods=['POST'])
def create_movie() -> Tuple[Response, int] | Response:
        movie_service = MovieService(MongoMovieRepository())
        
        if not request.get_json():
                return jsonify({"message": "No movie provided"}), 422
        
        movie = request.get_json()

        if isinstance(movie, list):
                return redirect(url_for('router.movies.create_movies'), code=307)

        try:
                response_message, status_code = movie_service.add_movie(movie)
                return jsonify({"message": response_message}), status_code
        except Exception:
                return jsonify({"message": INTERNAL_SERVER_ERROR_MSG}), 500

@movie_router.route('/insert-many', methods=['POST'])
def create_movies() -> Tuple[Response, int] | Response:
        movie_service = MovieService(MongoMovieRepository())

        if not request.get_json():
            return jsonify({"message": "No movies provided"}), 422
        
        movies = request.get_json()

        if isinstance(movies, dict) or (isinstance(movies, list) and len(movies) == 1):
                return redirect(url_for('router.movies.create_movie'), code=307)

        try:
                response_message, status_code = movie_service.add_many_movies(movies)
                return jsonify({"message": response_message}), status_code
        except Exception:
                return jsonify({"message": INTERNAL_SERVER_ERROR_MSG}), 500

@movie_router.route('', methods=['GET'])
def get_movies() -> Tuple[Response, int]:
        movie_service = MovieService(MongoMovieRepository())
        try:
                movies_limit = request.args.get('limit', default=10, type=int)
                movies_offset = request.args.get('offset', default=0, type=int)

                movies_raw = movie_service.get_all_movies(limit=movies_limit, offset=movies_offset)
                movies = [movie.model_dump() for movie in movies_raw]
                return jsonify(movies), 200
        except ValueError:
                return jsonify({"message": PAGINATION_ERROR_MSG}), 400
        except Exception:
                return jsonify({"message": INTERNAL_SERVER_ERROR_MSG}), 500
