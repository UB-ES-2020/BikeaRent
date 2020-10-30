from db import db

class BookingModel(db.Model):

	__tablename__ = 'booking'

	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
	motoid = db.Column(db.Integer, db.ForeignKey('motos.id'), nullable=False)
	startDate = db.Column(db.Date())
	endDate = db.Column(db.Date())
	totalTimeUsed = db.Column(db.Time())

	def __init__(self,userid,motoid,startDate,endDate,totalTimeUsed):
		self.userid = userid
		self.motoid = motoid
		self.startDate = startDate
		self.endDate = endDate
		self.totalTimeUsed = totalTimeUsed

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_id(cls, id):
		return booking.query.filter_by(id=id).first()

	@classmethod
	def find_by_username(cls, userid):
		return booking.query.filter_by(userid=userid)

	@classmethod
	def find_by_username(cls, motoid):
		return booking.query.filter_by(motoid=motoid)