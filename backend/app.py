from sqlite3.dbapi2 import Date

from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate

from backend.models.booking import BookingModel
from backend.models.moto import MotosModel
from backend.models.account import AccountsModel
from flask_restful import Resource, Api, reqparse
from backend.db import db

from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
#app.app_context().push()
migrate = Migrate(app,db)
db.init_app(app)
api = Api(app)



@app.route('/')
@app.route('/userlogin')
@app.route('/newaccount')
def login():
    return render_template("index.html")


# -------- Register  ---------------------------------------------------------- #
class Accounts(Resource):
    def get(self, username):
        user = AccountsModel.find_by_username(username)
        if user:
            return user.json(), 200
        else:
            return {'message': 'There is no client with username [{}] .'.format(username)}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('surname', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('dni', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('dataEndDrivePermission', type=Date, required=True, help="This field cannot be left blank")
        parser.add_argument('status', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('creditCard', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('availableMoney', type=int, required=True, help="This field cannot be left blank")
        parser.add_argument('type', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        user = AccountsModel.find_by_username(data['username'])
        if user:
            return {"message": "User already exists"}, 400
        else:
            new_user = AccountsModel(data['firstname'], data['surname'], data['email'], data['username'], data['dni'],
                                     data['dataEndDrivePermission'], data['status'], data['creditCard'], data['availableMoney'],
                                     data['type'])
            new_user.hash_password(data['password'])
            try:
                new_user.save_to_db()
                return new_user.json(), 200
            except:
                return {"message": "Database error"}, 500


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
        motos = MotosModel.query.filter_by(active = True)
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


api.add_resource(Accounts, '/account/<string:username>', '/account')
api.add_resource(AccountsList, '/accounts')

api.add_resource(MotosList, '/motos')

api.add_resource(Login, '/login')

api.add_resource(Booking, '/rent/<string:username>')
api.add_resource(BookingList, '/rents')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
