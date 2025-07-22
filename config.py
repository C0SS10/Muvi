from flask import Flask
from flask_cors import CORS
from app.routes.router import router

def create_app() -> Flask:
    application = Flask(__name__)
    CORS(application)
    application.register_blueprint(router)

    return application
