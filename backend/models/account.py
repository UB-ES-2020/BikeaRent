from db import db
from flask import g, current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth
from flask import g

auth = HTTPBasicAuth()

class AccountsModel(db.Model):
    __tablename__ = 'accounts'

    username = db.Column(db.String(30), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    dni = db.Column(db.String(9), unique=True, nullable=False)
    # role: admin/soporte/tecnico/user
    role = db.Column(db.String(10), nullable=False)
    available_money = db.Column(db.Integer)


    def __init__(self, username, email, dni, available_money=200, role = 'admin'):
        self.username = username
        self.email = email
        self.dni = dni
        self.available_money = available_money
        self.role = role


    def json(self):
        dictionary = {  'username': self.username,
                        'email': self.email,
                        'dni': self.dni,
                        'role': self.role}
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

@auth.verify_password
def verify_password(token, password):
    user = AccountsModel.verify_auth_token(token)
    g.user = user
    return user

