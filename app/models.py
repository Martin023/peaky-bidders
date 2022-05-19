from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    Bids = db.Column(db.Integer(), nullable=False, default=0)
    bids = db.relationship('Bids', backref='owned_user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String(length=12), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    bids = db.relationship('Bids', backref='item_bids', lazy='dynamic')

    def __repr__(self):
        return f'Item{self.name}{self.description}'


class Bids(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    price = db.Column(db.Integer(), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    item = db.Column(db.Integer(), db.ForeignKey('item.id'))
    date = db.Column(db.DateTime(), default=datetime.utcnow())

