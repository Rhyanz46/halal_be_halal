from datetime import datetime
from core.database import db
from core import slugify
from core.config import STATIC_FOLDER
from flask import request

user_foods = db.Table('user_foods',
                      db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

food_tags = db.Table('food_tags',
                      db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
                      db.Column('food_tag_id', db.Integer, db.ForeignKey('food_tag.id'), primary_key=True))

food_themes = db.Table('food_themes',
                      db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
                      db.Column('food_theme_id', db.Integer, db.ForeignKey('food_theme.id'), primary_key=True))


class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.TEXT)

    likes = db.relationship('User', secondary=user_foods, lazy='subquery', backref='food')
    images = db.relationship('FoodImage', lazy='subquery', backref='food')
    price = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    stock = db.Column(db.Integer, nullable=False)
    slug = db.Column(db.String(255), unique=True)
    sold = db.Column(db.BigInteger, default=0)
    view = db.Column(db.BigInteger, default=0)
    popularity = db.Column(db.BigInteger, default=0)
    ratting = db.Column(db.BigInteger, default=0)

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    category_id = db.Column(db.Integer, db.ForeignKey("food_category.id"))
    certificate_id = db.Column(db.Integer, db.ForeignKey("certificate.id"))
    currency_id = db.Column(db.Integer, db.ForeignKey("currency.id"))

    buyers = db.relationship('User', secondary=user_foods, lazy='subquery', backref='food_be_bought')
    tags = db.relationship('FoodTag', secondary=food_tags, lazy='subquery', backref='foods')
    themes = db.relationship('FoodTheme', secondary=food_themes, lazy='subquery', backref='foods')
    feed_backs = db.relationship('FoodFeedBack', backref='food', lazy=True)
    history = db.relationship('FoodHistory', backref='food')

    time_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Food, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __serialize__(self, with_img=False):
        short_desc = self.description
        if self.description:
            if len(self.description) >= 40:
                short_desc = self.description[:40].split(' ')
                short_desc.pop()
                short_desc = ' '.join(short_desc)
        tags = []
        for tag in self.tags:
            tags.append(tag.name)
        themes = []
        for theme in self.themes:
            theme.append(tag.name)
        packages = []
        for package in self.package:
            packages.append(package)
        feed_backs = []
        for i, feed_back in enumerate(self.feed_backs):
            feed_backs.append({
                "user": feed_back.user.username,
                "ratting": feed_back.ratting,
                "comment": feed_back.comment
            })
            if i == 5:
                break
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "short_description": short_desc,
            "ratting": self.ratting,
            "slug": self.slug,
            "prices": self.price,
            "discount": self.discount,
            "currency": self.currency.name if self.currency else None,
            "denote": self.currency.denote if self.currency else None,
            "packages": packages,
            "seller": {
                "id": self.store.id,
                "name": self.store.name,
                "image": self.store.img,
                # "address": self.store.address,
            },
            "attribute": {
                "like": len(self.likes),
                "view": self.view,
                "ratting": self.ratting,
                "sold": self.sold,
                "tags": tags,
                "themes": themes
            },
            "certificate": {
                "issuer": self.certificate.issuer if self.certificate else None,
                "date": self.certificate.date if self.certificate else None,
                "number": self.certificate.number if self.certificate else None
            },
            "feedbacks": feed_backs
        }
        if with_img:
            all_img = []
            for img in self.images:
                link = request.host_url + STATIC_FOLDER + '/' + img.link
                all_img.append(link)
            # img = []
            # main_img = None
            # for i, _img in enumerate(self.images):
            #     link = request.host_url + STATIC_FOLDER + '/' + _img.link
            #     if i:
            #         if _img.main:
            #             main_img = link
            #         else:
            #             img.append(link)
            #     if i == len(self.images) - 1:
            #         if not main_img:
            #             main_img = link
            #
            # all_img = {
            #     "main": main_img,
            #     "list": img
            # }
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