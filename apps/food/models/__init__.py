from datetime import datetime
from core.database import db
from core.config import STATIC_FOLDER
from flask import request, current_app

user_foods = db.Table('user_food',
                      db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.TEXT)

    ratting = db.Column(db.Integer, default=0)
    likes = db.relationship('User', secondary=user_foods, lazy='subquery', backref='food')
    images = db.relationship('FoodImage', lazy='subquery', backref='food')
    price = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    stock = db.Column(db.Integer, nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    category_id = db.Column(db.Integer, db.ForeignKey("food_category.id"))
    certificate_id = db.Column(db.Integer, db.ForeignKey("certificate.id"))

    buyers = db.relationship('User', secondary=user_foods, lazy='subquery', backref='food_be_bought')
    feed_backs = db.relationship('FoodFeedBack', backref='food', lazy=True)
    history = db.relationship('FoodHistory', backref='food')

    time_created = db.Column(db.DateTime, default=datetime.now())

    def __serialize__(self, with_img=False):
        print(current_app.config)
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ratting": self.ratting,
            "likes": self.likes,
            "price": self.price,
            "discount": self.discount,
            "seller": self.seller,
            "category": {
                "id": self.food_category.id,
                "name": self.food_category.name
            }
        }
        if with_img:
            img = []
            main_img = None
            for i, _img in enumerate(self.images):
                link = request.host_url + STATIC_FOLDER + '/' + _img.link
                if i:
                    if _img.main:
                        main_img = link
                    else:
                        img.append(link)
                if i == len(self.images) - 1:
                    if not main_img:
                        main_img = link

            all_img = {
                "main": main_img,
                "list": img
            }
            data.update({"image": all_img})
        return data

    # data = {
    #   "id": 12345,
    #   "name": "nama makanan",
    #   "desc": "deskripsi panjang",
    #   "shortDesc": "Deskripsi pendek",
    #   "images": [
    #     ""
    #   ],
    #   "slug": "",
    #   "prices": 123456,
    #   "currency": "IDR",
    #   "denote": "Rp",
    #   "packages": [
    #     123,
    #     123
    #   ],
    #   "discount": 0,
    #   "seller": {
    #     "id": 12345,
    #     "name": "nama seller",
    #     "image": "seller image",
    #     "address": "address"
    #   },
    #   "attribute": {
    #     "rating": 5,
    #     "popularity": 9,
    #     "like": 345,
    #     "view": 12345,
    #     "sold": 1236,
    #     "tags": [
    #       "makanan"
    #     ],
    #     "theme": [
    #       "lunch",
    #       "hot",
    #       "summer",
    #       "warm"
    #     ]
    #   },
    #   "certificate": {
    #     "issuer": "MUI",
    #     "date": "dd/mm/yy",
    #     "number": "nomer sertifikat"
    #   },
    #   "feedbacks": [
    #     {
    #       "user": "Fulan",
    #       "rating": 5,
    #       "comment": "enak cuy"
    #     }
    #   ]
    # }