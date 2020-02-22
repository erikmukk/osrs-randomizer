from flask import Flask
from flask_cors import CORS

def create_app(app_name="RANDOMIZER_API"):
    app = Flask(app_name)
    cors = CORS(app)
    from api.api import api
    app.register_blueprint(api)
    return app