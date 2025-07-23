from flask import Flask
from API.routes import math_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(math_bp)
    return app
