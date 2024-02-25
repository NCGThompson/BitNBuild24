from flask import Flask
from database import db
from database import User, Quadrat
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

def reset_database():
    """Drops all tables and recreates them"""
    with app.app_context():
        db.drop_all()
        db.create_all()

def add_sample_users():
    """Adds sample users to the database"""
    with app.app_context():
        users = [
            User(username='john_doe', email='john@example.com'),
            User(username='jane_doe', email='jane@example.com')
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()

def add_sample_quadrats():
    coordinateList = []
    random.seed(2)
    for _ in range(50):
        while (True):
            randInt = random.randrange(100000)
            locationDescription = "from " + str(randInt % 100) + "°N, " + str(randInt // 100) + "°W, to" + \
                            str((randInt % 100) + 1) + "°N, " + str((randInt // 100) + 1) + "°W"
            if not locationDescription in coordinateList:
                break
        coordinateList.append(locationDescription)
    assert(len(coordinateList) == 50)
    with app.app_context():
        db.session.add_all(
            [Quadrat(description=location, weight=1) for location in coordinateList]
        )

if __name__ == '__main__':
    should_reset = input("Reset the database? (y/n): ").lower() == 'y'
    if should_reset:
        reset_database()
        print("Database has been reset.")
    add_sample_users()
    add_sample_quadrats()
    print("Sample users added to the database.")
