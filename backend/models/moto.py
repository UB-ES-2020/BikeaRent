from db import db
from flask import g, current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth
from flask import g

auth = HTTPBasicAuth()

class MotosModel(db.Model):

    __tablename__ = 'Motos'

    id = db.column(db.Integer, primary_key = True)
    model = db.column(db.String(30))
    active = db.column(db.Boolean)
    charge = db.column(db.Integer)
    #position
    latitude = db.column(db.Float)
    longitude = db.column(db.Float)


    def __init__(model,active,charge,latitude,longitude):
        self.model = model
        self.active = active
        self.charge = charge
        self.latitude = latitude
        self.longitude = longitude