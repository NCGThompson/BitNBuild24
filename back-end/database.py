from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Quadrat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.PickleType, unique=True, nullable=False)
    weight = db.Column(db.Double, unique=False, nullable=True)

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer, db.ForeignKey('quadrat.id'), nullable=False)
    submitter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    measurement_time = db.Column(db.DateTime, unique=False, nullable=True)
    submition_time = db.Column(db.DateTime, unique=False, nullable=False)
    oak = db.Column(db.Double, unique=False, nullable=True)
    birch = db.Column(db.Double, unique=False, nullable=True)
    spruce = db.Column(db.Double, unique=False, nullable=True)