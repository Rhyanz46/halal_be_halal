from datetime import datetime
from core.database import db


class UserDetail(db.Model):
    __tablename__ = 'user_detail'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fullname = db.Column(db.String(90))
    phone_number = db.Column(db.BigInteger, unique=True)
    work_start_time = db.Column(db.Date, default=datetime.now())
    activate = db.Column(db.Boolean, default=True)
    created_time = db.Column(db.DateTime, default=datetime.now())

    addresses = db.relationship('Addresses', backref='user_detail')
    # job_history = db.relationship('FoodHistory', backref='user_detail')

    def __serialize__(self, id=None):
        if not id:
            return {
                "id": self.id,
                "user_id": self.user_id,
                "fullname": self.fullname,
                "address": self.address,
                "phone_number": self.phone_number,
                "work_start_time": self.work_start_time,
                "activate": self.activate,
                "created_time": self.created_time
            }
        user = UserDetail.query.get(id)
        if not user:
            return None
        return {
            "id": user.id,
            "user_id": user.user_id,
            "fullname": user.fullname,
            # "address": user.address,
            "phone_number": user.phone_number,
            "work_start_time": user.work_start_time,
            "activate": user.activate,
            "created_time": user.created_time
        }