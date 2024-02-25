from flask import Flask, jsonify, request
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

@app.route('/my-quadrats')
def my_quadrats():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username is required as a query parameter'}), 400

    # Look up the user by the provided username
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    quadrats_data = [{'id': quadrat.id, 'location': quadrat.location} for quadrat in user.quadrats]
    return jsonify({'quadrats': quadrats_data})


if __name__ == '__main__':
    app.run(debug=True)