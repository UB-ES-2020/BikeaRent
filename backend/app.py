from flask import Flask, render_template, url_for, request, redirect, session, request
from flask_restful import reqparse, Resource, Api
from backend.models.account import AccountsModel


app = Flask(__name__)
api = Api(app)

@app.route('/')
def login():
    return 'Hello World!'

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

if __name__ == '__main__':
    app.run(port=5000, debug=True)
