from flask_restful import Resource, reqparse

from models.account import AccountsModel


class AccountList(Resource):
    def get(self):
        users = AccountsModel.query.all()
        all_accounts = []
        for u in users:
            all_accounts.append(u.json())

        return {'accounts': all_accounts}, 200


class Account(Resource):
    # @auth.login_required()
    def get(self, username):
        user = AccountsModel.find_by_username(username)
        if user:
            return user.json(), 200
        else:
            return {'message': 'There is no client with username [{}] .'.format(username)}, 404

    # @auth.login_required()
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
        parser.add_argument('dataEndDrivePermission', type=str, required=True, help="This field cannot be left blank")
        # parser.add_argument('status', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('creditCard', type=str, required=True, help="This field cannot be left blank")
        # parser.add_argument('availableMoney', type=int, required=True, help="This field cannot be left blank")
        parser.add_argument('type', type=int, required=True, help="This field cannot be left blank")
        parser.add_argument('latitude', type=float, required=True, help="This field cannot be left blank")
        parser.add_argument('longitude', type=float, required=True, help="This field cannot be left blank")
        data = parser.parse_args()

        user = AccountsModel.find_by_username(data['username'])
        if user:
            return {"message": "User already exists"}, 400
        else:
            new_user = AccountsModel(data['firstname'], data['surname'], data['email'], data['username'], data['dni'],
                                     data['dataEndDrivePermission'], data['creditCard'],
                                     data['type'], data['latitude'], data['longitude'])
            new_user.hash_password(data['password'])
            try:
                new_user.save_to_db()
                return new_user.json(), 200
            except Exception as e:
                return {"message": "Database error"}, 500
                # return {e}

    def put(self, id):
        parser = reqparse.RequestParser()

        parser.add_argument('firstname', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('surname', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('dni', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('dataEndDrivePermission', type=str, required=True, help="This field cannot be left blank")
        parser.add_argument('creditCard', type=str, required=True, help="This field cannot be left blank")

        data = parser.parse_args()

        account = AccountsModel.find_by_id(id)
        if account:

            modified_account = AccountsModel(data['firstname'], data['surname'], data['email'], account.username,
                                             data['dni'], data['dataEndDrivePermission'], data['creditCard'],
                                             account.type, account.latitude, account.longitude)
            if account.firstname == modified_account.firstname and account.surname == modified_account.surname and account.email == modified_account.email and account.dni == modified_account.dni and account.dataEndDrivePermission == modified_account.dataEndDrivePermission and account.creditCard == modified_account.creditCard:
                return {"Error": "User {} is up to date".format(account.username)}, 400
            AccountsModel.modify_account(id, modified_account)
            return {"account": account.json()}, 200
        return {"Error": "Account with identifier {} not found".format(id)}, 404
