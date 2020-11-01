from flask import Flask
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse

from backend.db import db
from backend.models.booking import BookingModel
from backend.models.moto import MotosModel
from backend.models.account import AccountsModel

from datetime import datetime


class BookingList(Resource):
    def get(self):
        return BookingModel.list_orders()


class Booking(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('userid', type=int, required=True, help="The userid is required")
    parser.add_argument('motoid', type=int, required=True, help="The motoid is required")

    def get(self, username):
        rents = BookingModel.find_by_username(username)

        if len(rents) == 1:
            return {"rents": rents.json()}, 200
        if len(rents) > 1:
            return {"rents": [rent.json() for rent in rents]}, 200
        return {"Error": "There are no rents for username {}".format(username)}, 404

    def post(self, username):

        data = Booking.parser.parse_args()

        userid = data['userid']
        motoid = data['motoid']

        user = AccountsModel.find_by_username(username)
        moto_active = MotosModel.is_active(motoid)

        try:
            if user.availableMoney > 5:
                if moto_active is True:
                    new_rent = BookingModel(userid, motoid, datetime.now(), None, None)
                    MotosModel.change_status(motoid)

                    return {"new_rent": new_rent.json()}, 201
                return "Moto selected is not active", 400
            return "Not money enough", 400
        except:
            return "Something went wrong", 500


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# app.app_context().push()

api.add_resource(Booking, '/rent/<string:username>')
api.add_resource(BookingList, '/rents')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
