from flask import Flask
from models.moto import MotosModel
from flask_restful import Resource
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


class MotosList(Resource):
    def get(self):
        motos = MotosModel.query.filter_by(active = True)
        motosList = []
        for moto in motos:
            motosList.append(moto.json())
        return motosList

