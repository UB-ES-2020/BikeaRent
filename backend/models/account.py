
from backend.db import db
from flask import g, current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

status = ('active', 'notActive')
type = ('user', 'support', 'admin', 'technical')


class AccountsModel(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    dni = db.Column(db.String(30), unique=True, nullable=False)
    dataEndDrivePermission = db.Column(db.Date(), nullable=False)
    status = db.Column(db.Enum(*status))
    creditCard = db.Column(db.String(30), unique=True, nullable=False)
    availableMoney = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(*type), nullable=False)

    def __init__(self, firstname, surname, email, username, dni, dataEndDrivePermission, creditCard,
                 type, status='active', availableMoney=100):
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
            'type': self.type
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

    @classmethod
    def find_by_username(cls, username):
        return AccountsModel.query.filter_by(username=username).first()

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


@auth.verify_password
def verify_password(token, password):
    user = AccountsModel.verify_auth_token(token)
    g.user = user
    return user
