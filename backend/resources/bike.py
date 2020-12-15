from flask_restful import Resource, reqparse

from models.bike import MotosModel


class BikeList(Resource):
    def get(self):
        motos = MotosModel.query.filter_by(active=True)
        motosList = []
        for moto in motos:
            motosList.append(moto.json())
        return motosList


class Bike(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('model', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('active', type=bool, required=True, help="This field cannot be left blank")
    parser.add_argument('charge', type=int, required=True, help="This field cannot be left blank")
    parser.add_argument('latitude', type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('longitude', type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('plate', type=str, required=True, help="This field cannot be left blank")

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

    def put(self, id):
        data = self.parser.parse_args()

        bike = MotosModel.find_by_id(id)
        if bike:
            modified_bike = MotosModel(**data)
            if bike.model == modified_bike.model and bike.active == modified_bike.active and bike.charge == modified_bike.charge and bike.latitude == modified_bike.latitude and bike.longitude == modified_bike.longitude and bike.plate == modified_bike.plate:
                return {"Error": "Bike {} is up to date".format(bike.plate)}, 400
            MotosModel.modify_bike(id, modified_bike)
            return {"bike": bike.json()}, 200
        return {"Error": "Bike with identifier {} not found".format(id)}, 404
