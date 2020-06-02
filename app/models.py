from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


services_on_stations = db.Table('services_on_stations',
    db.Column('station_id', db.Integer, db.ForeignKey('stations.id')),
    db.Column('Services_id', db.Integer, db.ForeignKey('services.id'))
)


class Stations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coordinates = db.Column(db.String(100))
    number = db.Column(db.Integer)
    address = db.Column(db.String(200))
    photos = db.relationship('Photos', backref='station', lazy='dynamic')
    #services = db.relationship('Services', backref='station', lazy='dynamic')
    #goods = db.relationship('Goods', backref='station', lazy='dynamic')

    def __repr__(self):
        return f'<Station # {self.number}>'


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'))

    def __repr__(self):
        return f'<Photo {self.url}>'


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    #station_id = db.Column(db.Integer, db.ForeignKey('stations.id'))

    def __repr__(self):
        return f'<Service {self.title}>'


# class Join_services_on_stations(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     station_id = db.Column(db.Integer)
#     service_id = db.Column(db.Integer)
#
#     def __repr__(self):
#         return f'<connection {self.station_id} {self.service_id}>'


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    amount = db.Column(db.Integer)
    currency = db.Column(db.String(140))
    #station_id = db.Column(db.Integer, db.ForeignKey('stations.id'))

    def __repr__(self):
        return f'<Goods {self.title}>'

