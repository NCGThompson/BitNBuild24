from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_quadrat_association = db.Table('user_quadrat',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('quadrat_id', db.Integer, db.ForeignKey('quadrat.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    quadrats = db.relationship('Quadrat', secondary=user_quadrat_association, back_populates='users')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Quadrat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.PickleType, unique=True, nullable=False)
    weight = db.Column(db.Double, unique=False, nullable=True)
    users = db.relationship('User', secondary=user_quadrat_association, back_populates='quadrats')

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer, db.ForeignKey('quadrat.id'), nullable=False)
    submitter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    measurement_time = db.Column(db.DateTime, unique=False, nullable=True)
    submition_time = db.Column(db.DateTime, unique=False, nullable=False)
    oak = db.Column(db.Double, unique=False, nullable=True)
    birch = db.Column(db.Double, unique=False, nullable=True)
    spruce = db.Column(db.Double, unique=False, nullable=True)