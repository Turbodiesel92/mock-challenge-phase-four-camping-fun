from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    serialize_rules = ('-signups', '-activities.campers')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship("Signup", back_populates="camper")
    activities = association_proxy('signups', 'activity')

    @validates('name')
    def validate_name(self, name):
        if not name:
            raise ValueError('Failed name validation. Name must contain a value.')
        return name

    @validates('age')
    def validate_age(self, age):
        if age < 8 or age > 18:
            raise ValueError('Failed age validation. Age must be between 8 and 18.')
        return age


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-signups', '-campers.activities',
                       '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship("Signup", back_populates="activity")
    campers = association_proxy('signups', 'camper')


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    serialize_rules = ('-camper.signups', '-activity.signups',
                       '-camper.activities', '-activity.campers',
                       '-created_at', 'updated_at')

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    @validates('time')
    def validate_time(self, time):
        if time < 0 or time > 23:
            raise ValueError('Failed time validation. Time must be between 0 and 23.')
        return time