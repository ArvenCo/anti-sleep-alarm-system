from imports import SQLAlchemy, datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    event = db.Column(db.String, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())