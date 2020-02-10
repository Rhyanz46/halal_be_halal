from core.database import db


food_package = db.Table('food_package',
                        db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
                        db.Column('package_id', db.Integer, db.ForeignKey('package.id'), primary_key=True))

user_package = db.Table('user_package',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('package_id', db.Integer, db.ForeignKey('package.id'), primary_key=True))


class Package(db.Model):
    __tablename__: str = 'package'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart_item.id'))
    foods = db.relationship('Food', secondary=food_package, backref='package', lazy='subquery')
    users = db.relationship('User', secondary=user_package, backref='packages', lazy='subquery')
