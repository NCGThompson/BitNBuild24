from curses.ascii import US
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database import db, User

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)


@app.route("/")
def hello_world():
    return "<h3>Hello World</h3><h5>Current User Accounts</h5>\n" + \
        "<br/>".join([str(user) for user in User.query.all()])

if __name__ == '__main__':
    app.run(debug=True)