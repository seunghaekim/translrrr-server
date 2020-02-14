from flask import Flask
from flask_restful import Api
from translator.api import Translator
from flask_cors import CORS
from lib import config

app = Flask(__name__)
app.config.from_object('lib.config')

CORS(app, origins=config.CORS_ORIGIN_ALLOW_URL)

api = Api(app)

api.add_resource(Translator, '/translator')

if __name__ == "__main__":
    app.run()