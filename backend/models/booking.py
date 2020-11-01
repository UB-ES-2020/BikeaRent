from backend.db import db
from backend.models.account import AccountsModel


class BookingModel(db.Model):

	__tablename__ = 'booking'

	id = db.Column(db.Integer, primary_key=True)
	#userid = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
	#motoid = db.Column(db.Integer, db.ForeignKey('motos.id'), nullable=False)
	userid = db.Column(db.Integer)
	motoid = db.Column(db.Integer)
	startDate = db.Column(db.Date())
	endDate = db.Column(db.Date())
	totalTimeUsed = db.Column(db.Time())

    def __init__(self, userid, motoid, startDate, endDate, totalTimeUsed):
        self.userid = userid
        self.motoid = motoid
        self.startDate = startDate
        self.endDate = endDate
        self.totalTimeUsed = totalTimeUsed

    def json(self):
        return {
            'id': self.id,
            'userid': self.userid,
            'motoid': self.motoid,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'totalTimeUsed': self.totalTimeUsed
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # @classmethod
    # def find_by_id(cls, id):
    #     return cls.query.filter_by(id=id).first()
    #
    # @classmethod
    # def find_by_userid(cls, userid):
    #     return cls.query.filter_by(userid=userid).first()

    @classmethod
    def find_by_username(cls, username):
        return AccountsModel.find_by_username(username)

    # @classmethod
    # def find_by_motoid(cls, motoid):
    #     return cls.query.filter_by(motoid=motoid).first()

    @classmethod
    def list_orders(cls):
        orders = [order.json() for order in cls.query.all()]
        return {"orders": orders}