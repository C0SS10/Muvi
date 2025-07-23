import os
from dotenv import load_dotenv
from pytest import fixture
from app.config import create_app

load_dotenv(".env.test", override=True)
os.environ["ENVIRONMENT"] = "test"

@fixture()
def app():
    # Create a test instance of the Flask application
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DEBUG": False,
    })

    return app

@fixture()
def client(app):
    # Create a test client, that can be used to make requests
    client = app.test_client()

    return client