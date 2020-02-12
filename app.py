from flask import Flask
from flask_restful import Api
from translator.api import Translator

app = Flask(__name__)
app.config.from_object('lib.config')
api = Api(app)

api.add_resource(Translator, '/translator')

if __name__ == "__main__":
    app.run()