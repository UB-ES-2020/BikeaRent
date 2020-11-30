from sqlite3.dbapi2 import Date

from flask import Flask, render_template
from flask_migrate import Migrate
from models.booking import BookingModel
from models.moto import MotosModel
from models.account import AccountsModel, auth
from flask_restful import Resource, Api, reqparse
from db import db
from flask_cors import CORS

from decouple import config as config_decouple
from config import config

import time

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

environment = config['development']
if config_decouple('PRODUCTION', cast=bool, default=False):
    environment = config['production']

app.config.from_object(environment)

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

# app.app_context().push()


@app.route('/')
@app.route('/home')
def render_vue():
    return render_template("index.html")


class Motos(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('model', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('active', type=bool, required=True, help="This field cannot be left blank")
    parser.add_argument('charge', type=int, required=True, help="This field cannot be left blank")
    parser.add_argument('latitude', type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('longitude', type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('plate',type=str,required = True,help = "This field cannot be left blank")

    def get(self, id):
        moto = MotosModel.find_by_id(id)
        if moto:
            return {"moto": moto.json()}, 200
        return {"Error": "Moto with identifier {} not found".format(id)}, 404

    def post(self):
        data = self.parser.parse_args()

        try:
            new_moto = MotosModel(**data)
            new_moto.save_to_db()
            return "Moto created successfully", 201
        except:
            return {"Error": "An error occurred creating moto"}, 500


# -------- Register  ---------------------------------------------------------- #
class Accounts(Resource):
    def get(self, username):
        user = AccountsModel.find_by_username(username)
        if user:
            return user.json(), 200
        else:
            return {'message': 'There is no client with username [{}] .'.format(username)}, 404

    def delete(self, username):
        user = AccountsModel.find_by_username(username)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {'message': "User deleted"}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('surname', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('dni', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('dataEndDrivePermission',type=str, required=True, help="This field cannot be left blank")
        #parser.add_argument('status', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('creditCard', type=str, required=True, help="This field cannot be left blank")
        #######parser.add_argument('availableMoney', type=int, required=True, help="This field cannot be left blank")
        parser.add_argument('type', type=int, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        user = AccountsModel.find_by_username(data['username'])
        if user:
            return {"message": "User already exists"}, 400
        else:
            new_user = AccountsModel(data['firstname'], data['surname'], data['email'], data['username'], data['dni'],
                                     data['dataEndDrivePermission'], data['creditCard'],
                                     data['type'])
            new_user.hash_password(data['password'])
            try:
                new_user.save_to_db()
                return new_user.json(), 200
            except Exception as e:
                return {"message": "Database error"}, 500
                #return {e}


# -------- Accounts List  ---------------------------------------------------------- #
class AccountsList(Resource):
    def get(self):
        users = AccountsModel.query.all()
        all_accounts = []
        for u in users:
            all_accounts.append(u.json())

        return {'accounts': all_accounts}, 200


# -------- Login  ---------------------------------------------------------- #
class Login(Resource):
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

        data = parser.parse_args()
        user = AccountsModel.find_by_username(data['username'])

        if user:
            if user.verify_password(data['password']):
                token = user.generate_auth_token()
                return {'token': token.decode('ascii')}, 200
            else:
                return {"message": "Password not correct"}, 400
        else:
            return {"message": "User not found"}, 404


# -------- MotosList  ---------------------------------------------------------- #
class MotosList(Resource):
    def get(self):
        motos = MotosModel.query.filter_by(active=True)
        motosList = []
        for moto in motos:
            motosList.append(moto.json())
        return motosList


# -------- BookingList  ---------------------------------------------------------- #
class BookingList(Resource):
    def get(self):
        return BookingModel.list_orders()


# -------- Booking  ---------------------------------------------------------- #
class Booking(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('userid', type=int, required=True, help="The userid is required")
    parser.add_argument('motoid', type=int, required=True, help="The motoid is required")

    def get(self, userid):
        rents = BookingModel.find_by_userid(userid)

        if len(rents) == 1:
            return {"rents": rents.json()}, 200
        if len(rents) > 1:
            return {"rents": [rent.json() for rent in rents]}, 200
        return {"Error": "There are no rents for user with id {}".format(userid)}, 404

    def post(self):

        data = Booking.parser.parse_args()

        userid = data['userid']
        motoid = data['motoid']

        user = AccountsModel.find_by_id(userid)
        moto_active = MotosModel.is_active(motoid)

        try:
            if user.availableMoney > 5:
                if moto_active is True:
                    new_rent = BookingModel(userid, motoid, time.time(), None, None, None)
                    MotosModel.change_status(motoid)

                    return {"new_rent": new_rent.json()}, 201
                return "Moto selected is not active", 400
            return "Not money enough", 400
        except:
            return "Something went wrong", 500

    def put(self):

        data = Booking.parser.parse_args()

        userid = data['userid']
        motoid = data['motoid']

        try:
            admin_user = AccountsModel.find_by_username('admin')
            user = AccountsModel.find_by_id(userid)

            if user is None:
                return "User not found", 404

            book = BookingModel.finalize_book(userid, motoid)
            MotosModel.change_status(motoid)

            admin_user.availableMoney += book.price
            user.availableMoney -= book.price

            return "Booking finalized correctly", 201
        except:
            return "Something went wrong", 500

api.add_resource(Accounts, '/account/<string:username>', '/account')
api.add_resource(AccountsList, '/accounts')

api.add_resource(MotosList, '/bikes')
api.add_resource(Motos,'/bike','/bike/<int:id>')

api.add_resource(Login, '/login')

api.add_resource(Booking, '/rent')
api.add_resource(BookingList, '/rents')

if __name__ == '__main__':
    app.run(port=5000, debug=True)




