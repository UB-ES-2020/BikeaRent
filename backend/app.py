from flask import Flask, render_template, g, url_for, request, redirect, session, request
from flask_restful import reqparse, Resource, Api
from flask_migrate import Migrate
from backend.models.account import AccountsModel
from backend.models.order import OrdersModel
from db import db


app = Flask(__name__)

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
    def gest(self, username):
        user = AccountsModel.find_by_username(username)
        if user:
            return user.json(), 200
        else:
            return {'message': 'There is no client with username [{}] .'.format(username)}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('dni', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('iban', type=str, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        c = AccountsModel.find_by_email(data['email'])
        if c:
            return {"message": "This email was registered before."}, 400
        else:
            new_user = AccountsModel(data['email'])
            new_user.hash_password(data['password'])
            new_user = AccountsModel(data['username'])
            new_user = AccountsModel(data['dni'])
            new_user = AccountsModel(data['iban'])
            try:
                new_user.save_to_db()
                return new_user.json(), 200
            except:
                return {"message": "Database error"}, 500

    def delete(self, username):
        if username == g.user.username:
            user = AccountsModel.find_by_username(username)
            if user: #OrdersModel -> nombre provisional
                user_order = OrdersModel.find_by_username(username)
                for usr in user_order:
                    usr.delete_from_db()
                    try:
                        usr.save_to_db()
                    except:
                        return {'message': "Database Error2"}, 500
                user.delete_from_db()
                try:
                    user.save_to_db()
                except:
                    return {'message': "DataBase Error"}, 500
                return {'message': "User with username [{}] removed".format(username)}, 200
            else:
                return {'message': "User with username [{}] Not found".format(username)}, 404
        else:
            return {"message": "User match not found"}, 400


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

# -------- Logout  ---------------------------------------------------------- #
class Logout(Resource):
    def logout(self):
        return render_template("/index")



api.add_resource(Accounts, '/account/<string:username>', '/account')
api.add_resource(AccountsList, '/accounts')

api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
