from db import db
from flask import g, current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


class AccountsModel(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    dni = db.Column(db.String(30), unique=True, nullable=False)
    dataEndDrivePermission = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Boolean, nullable=False)  # true = active, false = notActive
    creditCard = db.Column(db.String(30), unique=True, nullable=False)
    availableMoney = db.Column(db.Float, nullable=False)
    type = db.Column(db.Integer, nullable=False)  # 0=user, 1 = support, 2= technical, 3 = admi
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, firstname, surname, email, username, dni, dataEndDrivePermission, creditCard,
                 type, latitude, longitude, status=True, availableMoney=100):
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
        self.latitude = latitude
        self.longitude = longitude

    def json(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'surname': self.surname,
            'email': self.email,
            'username': self.username,
            'dni': self.dni,
            'dataEndDrivePermission': self.dataEndDrivePermission,
            'status': self.status,
            'creditCard': self.creditCard,
            'availableMoney': self.availableMoney,
            'type': self.type,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return AccountsModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return AccountsModel.query.filter_by(email=email).first()

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.secret_key, expires_in=expiration)
        return s.dumps({'username': self.username})

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(current_app.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        user = cls.query.filter_by(username=data['username']).first()

        return user

    @classmethod
    def find_by_id(cls, id):
        return AccountsModel.query.filter_by(id=id).first()

    @classmethod
    def modify_account(cls, id, modified_account):
        account = cls.query.filter_by(id=id).first()

        if account.firstname != modified_account.firstname:
            account.firstname = modified_account.firstname
        if account.surname != modified_account.surname:
            account.surname = modified_account.surname
        if account.email != modified_account.email:
            account.email = modified_account.email
        if account.dni != modified_account.dni:
            account.dni = modified_account.dni
        if account.dataEndDrivePermission != modified_account.dataEndDrivePermission:
            account.dataEndDrivePermission = modified_account.dataEndDrivePermission
        if account.creditCard != modified_account.creditCard:
            account.creditCard = modified_account.creditCard

        db.session.add(account)
        db.session.commit()


@auth.verify_password
def verify_password(token, password):
    user = AccountsModel.verify_auth_token(token)
    g.user = user
    return user
