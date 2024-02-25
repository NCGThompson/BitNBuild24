from datetime import datetime
from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    assignments = db.relationship('Assignment', back_populates='user')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Quadrat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, unique=True, nullable=False)
    weight = db.Column(db.Double, unique=False, nullable=True, default=1)
    assignments = db.relationship('Assignment', back_populates='quadrat')

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quadrat_id = db.Column(db.Integer, db.ForeignKey('quadrat.id'), nullable=False)
    assignment_date = db.Column(db.DateTime, unique=True, nullable=True)
    due_date = db.Column(db.DateTime, unique=False, nullable=True)
    user = db.relationship('User', back_populates='assignments')
    quadrat = db.relationship('Quadrat', back_populates='assignments')

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer, db.ForeignKey('quadrat.id'), nullable=False)
    submitter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    measurement_time = db.Column(db.DateTime, unique=False, nullable=True)
    submition_time = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    oak = db.Column(db.Double, unique=False, nullable=True)
    birch = db.Column(db.Double, unique=False, nullable=True)
    spruce = db.Column(db.Double, unique=False, nullable=True)