from app import db # login
from flask_login import UserMixin
import os
import base64
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash, check_password_hash
import jwt

import time


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        #return check_password_hash(self.password_hash, password)
        return self.password_hash == password


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')


    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token


    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


'''

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

'''


class Sticker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(150))
    link = db.Column(db.String(150))


    def save(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def getAll():
        stickers = Sticker.query.all()
        result = []
        for sticker in stickers:
            obj = {
                'id': sticker.id,
                'path': sticker.path,
                'link': sticker.link
            }
            result.append(obj)
        return result


class PromoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(150))
    sticker_id = db.Column(db.Integer, db.ForeignKey('sticker.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def getAll():
        promoCodes = PromoCode.query.all()
        result = []
        for code in promoCodes:
            obj = {
                'id': code.id,
                'value': code.value,
                'sticker_id': code.sticker_id
            }
            result.append(obj)
        return result
