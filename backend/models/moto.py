from db import db
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


class MotosModel(db.Model):
    __tablename__ = 'motos'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(30))
    active = db.Column(db.Boolean)
    charge = db.Column(db.Integer)
    # position
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, model, active, charge, latitude, longitude):
        self.model = model
        self.active = active
        self.charge = charge
        self.latitude = latitude
        self.longitude = longitude

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
        if moto.active is False:
            moto.active = True

        db.session.add(moto)
        db.session.commit()
