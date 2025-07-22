from flask import Flask
from flask_cors import CORS
from app.routes.router import router
import logging

def create_app() -> Flask:
    application = Flask(__name__)
    CORS(application)
    application.register_blueprint(router)

    # Desactiva el banner de Flask (opcional)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    return application

# Banner to display that shows 'MUVI'
BANNER: str = r"""
_|      _|  _|    _|  _|      _|  _|_|_|  
_|_|  _|_|  _|    _|  _|      _|    _|    
_|  _|  _|  _|    _|  _|      _|    _|    
_|      _|  _|    _|    _|  _|      _|    
_|      _|    _|_|        _|      _|_|_|

                MUVI
"""