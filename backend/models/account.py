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

    __tablename__ = 'Accounts'

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

    def __init__(firstname,surname,email,username,password,dni,dataEndDrivePermission,status,creditCard,availableMoney,type):
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.username = username
        self.password = password
        self.dni = dni
        self.dataEndDrivePermission = dataEndDrivePermission
        self.status = status
        self.creditCard = creditCard
        self.availableMoney = availableMoney
        self.type = type
"""
    def __init__(self, username, available_money=200, is_admin=0):
        self.username = username
        self.available_money = available_money
        self.is_admin = is_admin
"""

