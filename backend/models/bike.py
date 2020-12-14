from db import db
from flask_httpauth import HTTPBasicAuth
from math import radians, sin, cos, acos

auth = HTTPBasicAuth()


class MotosModel(db.Model):
    __tablename__ = 'motos'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(30), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    charge = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    plate = db.Column(db.String(8), unique=True, nullable=False)

    def __init__(self, model, active, charge, latitude, longitude, plate, position="Passeig de Gracia, 55, Barcelona"):
        self.model = model
        self.active = active
        self.charge = charge
        self.latitude = latitude
        self.longitude = longitude
        self.position = position
        self.plate = plate

    def json(self):
        return {
            'id': self.id,
            'model': self.model,
            'active': self.active,
            'charge': self.charge,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'plate': self.plate
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return MotosModel.query.filter_by(id=id).first()

    @classmethod
    def is_active(cls, id):
        moto = cls.query.filter_by(id=id).first()
        return moto.active

    @classmethod
    def change_status(cls, id):
        moto = cls.query.filter_by(id=id).first()
        if moto.active is True:
            moto.active = False
        elif moto.active is False:
            moto.active = True

        db.session.add(moto)
        db.session.commit()

    @classmethod
    def distMotoUser(cls, user, moto):
        # Ej:
        coordUser = [41.386422, 2.16407]  # UB #0.45 km
        coordMoto = [41.387872, 2.170001]  # ECI - Pz Cat.

        # coordMoto = [moto.latitude,moto.longitude]
        # coordUser = [user.latitude, user.longitude]

        slat = radians(coordUser[0])
        slon = radians(coordUser[1])
        elat = radians(coordMoto[0])
        elon = radians(coordMoto[1])

        # Distance in kilometer
        return 6371.01 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))

    @classmethod
    def modify_bike(cls, id, modified_bike):
        bike = cls.query.filter_by(id=id).first()

        if bike.model != modified_bike.model:
            bike.model = modified_bike.model
        if bike.active != modified_bike.active:
            bike.active = modified_bike.active
        if bike.charge != modified_bike.charge:
            bike.charge = modified_bike.charge
        if bike.latitude != modified_bike.latitude:
            bike.latitude = modified_bike.latitude
        if bike.longitude != modified_bike.longitude:
            bike.longitude = modified_bike.longitude
        if bike.plate != modified_bike.plate:
            bike.plate = modified_bike.plate

        db.session.add(bike)
        db.session.commit()
