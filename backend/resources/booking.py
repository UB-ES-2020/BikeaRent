from flask_restful import Resource, reqparse

from models.bike import MotosModel
from models.account import AccountsModel
from models.booking import BookingModel

from datetime import datetime


class BookingList(Resource):
    def get(self):
        return BookingModel.list_orders()


class Booking(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('userid', type=int, required=True, help="The userid is required")
    parser.add_argument('bikeid', type=int, required=True, help="The bikeid is required")

    def get(self, userid):
        rents = BookingModel.find_by_userid(userid)

        if len(rents) == 1:
            return {"rents": rents.json()}, 200
        if len(rents) > 1:
            return {"rents": [rent.json() for rent in rents]}, 200
        return {"Error": "There are no rents for user with id {}".format(userid)}, 404

    def post(self):
        data = self.parser.parse_args()

        userid = data['userid']
        bikeid = data['bikeid']

        user = AccountsModel.find_by_id(userid)
        bike = MotosModel.find_by_id(bikeid)

        if user is None:
            return "User not found", 404

        if bike is None:
            return "Bike not found", 404

        moto_active = MotosModel.is_active(bikeid)

        try:
            if user.availableMoney > 5:
                if moto_active is True:
                    new_rent = BookingModel(userid, bikeid, None, None, None)
                    new_rent.startDate = datetime.now()
                    new_rent.save_to_db()

                    MotosModel.change_status(bikeid)

                    return {"new_rent": new_rent.json()}, 201
                return "Moto selected is not active", 400
            return "Not money enough", 400
        except:
            return "Something went wrong", 500

    def put(self):

        data = self.parser.parse_args()

        userid = data['userid']
        bikeid = data['bikeid']

        user = AccountsModel.find_by_id(userid)
        bike = MotosModel.find_by_id(bikeid)

        if user is None:
            return "User not found", 404
        if bike is None:
            return "Bike not found", 404

        try:
            admin_user = AccountsModel.find_by_username('admin')

            if admin_user:
                book = BookingModel.finalize_book(userid, bikeid)
                if book is None:
                    return "No renting found", 404
                MotosModel.change_status(bikeid)

                admin_user.availableMoney += book.price
                admin_user.save_to_db()
                user.availableMoney -= book.price
                user.save_to_db()

                return {"finalized_rent": book.json()}, 201
            return "Admin user not found", 404
        except:
            return "Something went wrong", 500
