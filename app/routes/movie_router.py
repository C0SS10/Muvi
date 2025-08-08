from bson import ObjectId
from flask import Blueprint, redirect, request, jsonify, url_for
from werkzeug.wrappers.response import Response
from typing import Tuple
from app.domain.services.movie_services import MovieService
from app.infrastructure.mongo_movie_repository import MongoMovieRepository
from app.utils.parser_query_params import parse_query_params

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
        filters, limit, offset, sort_by, order = parse_query_params(request.args)
        
        movies = movie_service.get_movies(
            filters=filters,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            order=order
        )

        if not movies:
            return jsonify({"message": "No movies found"}), 404

        return jsonify([m.model_dump() for m in movies]), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception:
        return jsonify({"message": INTERNAL_SERVER_ERROR_MSG}), 500

@movie_router.route('/<id>', methods=['GET'])
def get_movie_by_id(id: str) -> Tuple[Response, int]:
        movie_service = MovieService(MongoMovieRepository())
        try:
                movie_id = ObjectId(id)
                movie = movie_service.get_movie_by_id(movie_id)

                if not movie:
                        return jsonify({"message": "Movie not found"}), 404

                return jsonify(movie.model_dump()), 200
        except ValueError:
                return jsonify({"message": "Invalid movie ID"}), 400
        except Exception:
                return jsonify({"message": INTERNAL_SERVER_ERROR_MSG}), 500