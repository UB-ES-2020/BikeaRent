from db import db
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

status = ('active','notActive')
type = ('user','support','admin','technical')

class AccountsModel(db.Model):

    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    email = db.Column(db.String(30))
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    dni = db.Column(db.String(30))
    dataEndDrivePermission = db.Column(db.Date())
    status = db.Column(db.Enum(*status))
    creditCard = db.Column(db.String(30))
    availableMoney = db.Column(db.Integer)
    type = db.Column(db.Enum(*type))


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



