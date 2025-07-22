from flask import Blueprint
from app.routes.movie_router import movie_router

router = Blueprint('router', __name__)

router.register_blueprint(movie_router, url_prefix='/api/movies')