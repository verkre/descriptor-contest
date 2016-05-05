from flask_sqlalchemy import SQLAlchemy
from . import app
db = SQLAlchemy(app)


class Contest(db.Model):
    __tablename__='contests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Contest %r>' % self.name
    
