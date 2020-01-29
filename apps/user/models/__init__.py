from datetime import datetime
from core.database import db

from .details import UserDetail


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # category_access_id = db.Column(db.Integer, db.ForeignKey("category_access.id"))
    username = db.Column(db.String(90), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_detail = db.relationship('UserDetail', uselist=False, backref='user')
    food_feed_backs = db.relationship('FoodFeedBack', backref='user', lazy=True)
    created_time = db.Column(db.DateTime, default=datetime.now())

    def __serialize__(self, detail=False):
        if detail:
            social_medias = []
            for social_media in self.user_detail.social_medias:
                social_medias.append({
                    "provider": social_media.provider,
                    "uid": social_media.uid,
                    "image": social_media.image
                })
            addresses = []
            for address in self.user_detail.addresses:
                addresses.append({
                  "name": address.name,
                  "latitude": address.latitude,
                  "longitude": address.longitude,
                  "address": address.address,
                  "note": address.note
                })
            data = {
                "id": self.id,
                "username": self.username,
                "fullname": self.user_detail.fullname,
                "email": self.email,
                "phone": self.user_detail.phone_number,
                "rating": self.user_detail.ratting,
                "image": self.user_detail.image,
                "social": social_medias,
                "addresses": addresses
            }
        else:
            data = {
                "id": self.id,
                # "category_access_id": self.category_access_id,
                "username": self.username,
                "email": self.email
            }
        return data
