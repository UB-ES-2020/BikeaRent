from db import db
from models.account import AccountsModel

import time

class BookingModel(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    # userid = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    # motoid = db.Column(db.Integer, db.ForeignKey('motos.id'), nullable=False)
    userid = db.Column(db.Integer,nullable=False)
    motoid = db.Column(db.Integer,nullable=False)
    startDate = db.Column(db.Date(),nullable=False)
    endDate = db.Column(db.Date(),nullable=True)
    totalTimeUsed = db.Column(db.Integer,nullable=True)
    price = db.Column(db.Float(),nullable=True)

    def __init__(self, userid, motoid, startDate, endDate, totalTimeUsed, price):
        self.userid = userid
        self.motoid = motoid
        self.startDate = startDate
        self.endDate = endDate
        self.totalTimeUsed = totalTimeUsed
        self.price = price

    def json(self):
        self.startDate = self.startDate.strftime('%Y-%m-%d %H:%M:%S.%f')
        if self.endDate != None:
            self.endDate = self.endDate.strftime('%Y-%m-%d %H:%M:%S.%f')
        return {
            'id': self.id,
            'userid': self.userid,
            'motoid': self.motoid,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'totalTimeUsed': self.totalTimeUsed,
            'price': self.price
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.filter_by(userid=userid).first()

    @classmethod
    def find_by_username(cls, username):
        return AccountsModel.find_by_username(username)

    @classmethod
    def find_by_motoid(cls, motoid):
        return cls.query.filter_by(motoid=motoid).first()

    @classmethod
    def find_by_userid_motoid(cls, userid, motoid):
        return cls.query.filter_by(userid=userid, motoid=motoid).all()

    @classmethod
    def list_orders(cls):
        orders = [order.json() for order in cls.query.all()]
        return {"orders": orders}

    @classmethod
    def finalize_book(cls, userid, motoid):
        books = cls.find_by_userid_motoid(userid, motoid)
        for book in books:
            if book.endDate is None:
                pricePerSecond = 0.008  # should be a configuration

                book.endDate = time.time()
                book.totalTimeUsed = book.endDate - book.startDate
                book.price = book.totalTimeUsed * pricePerSecond

                book.save_to_db()

        return book
