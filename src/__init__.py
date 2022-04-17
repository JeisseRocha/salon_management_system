from flask import Flask
from flask_cors import CORS

from src.exception import GlobalException
from src.routes import register_routes


def create_app():
    app = Flask(__name__)
    # route
    register_routes(app)
    GlobalException.handle(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app