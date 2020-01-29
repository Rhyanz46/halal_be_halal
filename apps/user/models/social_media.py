from datetime import datetime
from core.database import db


class SocialMedia(db.Model):
    __tablename__ = 'social_media'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.TEXT)
    image = db.Column(db.TEXT)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider = db.Column(db.String(90))
    link = db.Column(db.TEXT)
    user_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'))
    created_time = db.Column(db.DateTime, default=datetime.now())
