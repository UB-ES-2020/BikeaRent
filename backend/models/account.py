from db import db
from flask import g, current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth
from flask import g

auth = HTTPBasicAuth()

class AccountsModel(db.Model):
    __tablename__ = 'accounts'

    email = db.Column(db.String(50), primary_key = True, unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    username = db.Column(primary_key=True, unique=True, nullable=False)
    dni = db.Column(db.String(9),unique=True, nullable=False)
    iban = db.Column(db.String(24),nullable=False)

    def __init__(self, email, username, password, dni, iban):
        self.email = email
        self.username = username
        self.password = password
        self.dni = dni
        self.iban = iban

    def json(self):
        dictionary = {  'email': self.email,
                        'username': self.username,
                        'password': self.password,
                        'dni': self.dni,
                        'iban': self.iban}
        return dictionary

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

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

    @auth.verify_password
    def verify_password(token, password):
        user = AccountsModel.verify_auth_token(token)
        g.user = user
        return user
