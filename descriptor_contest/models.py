from __future__ import unicode_literals

from flask_sqlalchemy import SQLAlchemy
from . import app

db = SQLAlchemy(app)

class Contest(db.Model):
    __tablename__ = 'contests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode())
    
    def __repr__(self):
        return '<Contest(name=%r)>' % self.name
    

class Descriptor(db.Model):
    __tablename__ = 'descriptors'
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Unicode())
    
    contest_id = db.Column(db.Integer, db.ForeignKey(Contest.id))
    contest = db.relationship(Contest, backref=db.backref('descriptors', lazy='dynamic'))
    
    def __repr__(self):
        return '<Descriptor(value=%r)>' % self.value
    

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Unicode())
    
    def __repr__(self):
        return '<User(user_name=%r)>' % self.user_name

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, backref=db.backref('answers', lazy='dynamic'))
    
    higher_ranked_descriptor_id = db.Column(db.Integer, db.ForeignKey(Descriptor.id))
    higher_ranked_descriptor = db.relationship(Descriptor,
        foreign_keys=higher_ranked_descriptor_id,
        backref=db.backref('higher_ranked_answers', lazy='dynamic'))
    
    lower_ranked_descriptor_id = db.Column(db.Integer, db.ForeignKey(Descriptor.id))
    lower_ranked_descriptor = db.relationship(Descriptor,
        foreign_keys=lower_ranked_descriptor_id,
        backref=db.backref('lower_ranked_answers', lazy='dynamic'))
    
    def __repr__(self):
        return '<Answer(higher_ranked_descriptor=%r, lower_ranked_descriptor=%r)>' \
             % (self.higher_ranked_descriptor, self.lower_ranked_descriptor)
