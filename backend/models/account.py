from db import db
from flask import g, current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth
from flask import g

auth = HTTPBasicAuth()

status = ('','')
type = ('user','support','admin','technical')

class AccountsModel(db.Model):

    __tablename__ = 'accounts'

    id = db.column(db.Integer, primary_key = True)
    firstname = db.column(db.String(30))
    surname = db.column(db.String(30))
    email = db.column(db.String(30))
    username = db.column(db.String(30))
    password = db.column(db.String(30))
    dni = db.column(db.String(30))
    dataEndDrivePermission = db.column(db.Date())
    status = db.column(db.Enum(*status))
    creditCard = db.column(db.String(30))
    availableMoney = db.column(db.Integer)
    type = db.column(db.Enum(*type))


    def __init__(self,firstname,surname,email,username,dni,dataEndDrivePermission,status,creditCard,availableMoney,type):
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.username = username
        self.dni = dni
        self.dataEndDrivePermission = dataEndDrivePermission
        self.status = status
        self.creditCard = creditCard
        self.availableMoney = availableMoney
        self.type = type

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return AccountsModel.query.filter_by(username=username).first()



