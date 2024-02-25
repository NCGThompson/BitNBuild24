from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db, User, Quadrat, Assignment

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

    quadrats_data = []
    for assignment in user.assignments:
        quadrat = assignment.quadrat
        quadrats_data.append({
            'assignment_id': assignment.id,
            'assigned_date': assignment.assignment_date,
            'due_date': assignment.due_date,
            'quadrat_id': quadrat.id,
            'location': quadrat.description,
        })
    return jsonify({'quadrats': quadrats_data})

# TODO: fix unsupported media type
@app.route('/assign-quadrat', methods=['POST'])
def assign_quadrat():
    data = request.form

    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Try to find a quadrat without any assignments
    unassigned_quadrat = Quadrat.query.filter(~Quadrat.assignments.any()).first()

    if unassigned_quadrat:
        # If there's an unassigned quadrat, create a new assignment for it
        new_assignment = Assignment(user_id=user.id, quadrat_id=unassigned_quadrat.id)
        db.session.add(new_assignment)
    else:
        # Find the quadrat with the earliest due date among all assignments
        earliest_due_quadrat = Quadrat.query.join(Assignment).order_by(Assignment.due_date.asc()).first()

        # Check if the earliest due date has not passed
        if earliest_due_quadrat and earliest_due_quadrat.assignments[-1].due_date > datetime.utcnow():
            # If the due date hasn't passed, do not assign
            return jsonify({'message': 'No quadrats available for assignment'}), 409
        elif earliest_due_quadrat:
            # Create a new assignment with the quadrat that has the earliest due date
            new_assignment = Assignment(user_id=user.id, quadrat_id=earliest_due_quadrat.id)
            db.session.add(new_assignment)
        else:
            return jsonify({'message': 'No quadrats available'}), 409

    db.session.commit()
    return jsonify({'message': 'Quadrat assigned successfully', 'quadrat_id': new_assignment.quadrat_id}), 201

@app.route('/submit-assignment')
def submit_assignment():
    # Render an HTML form for GET requests
    return '''
    <form action="/assign-quadrat" method="post">
        Username: <input type="text" name="username"><br>
        <input type="submit" value="Assign Quadrat">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)