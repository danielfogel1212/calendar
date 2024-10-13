from flask import jsonify, request
from flask_restful import Resource
from models import Birthday, Event, User,Branch ,db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager,get_jwt_identity
from werkzeug.security import generate_password_hash


# Initialize the JWT manager in your app (in your main app file)


class BirthDayResource(Resource):
    @jwt_required()
    def post(self):
     
            data = request.get_json()  # Get the JSON data from the request
            new_birthday = Birthday(name=data['name'], date=data['date'],branch_id=data['branch_id'])  # Create a new Birthday instance
            db.session.add(new_birthday)  # Add the new birthday to the session
            db.session.commit()  # Commit the session to the database
            return {'message': 'יום הולדת נוסף בהצלחה'}, 201  # Return a success message

    def get(self):
        # Fetch the branch_id from the query parameters, if provided
        branch_id = request.args.get('branch_id')

        # If a branch_id is provided, filter by branch, otherwise fetch all birthdays
        if branch_id:
            birthdays = Birthday.query.filter_by(branch_id=branch_id).all()
        else:
            birthdays = Birthday.query.all()

        # Prepare the result list with birthday details
        result = []
        for birthday in birthdays:
            birthday_data = {
                'date': birthday.date,
                'name': birthday.name,
                 'branch': {
                    'id': birthday.branch.id,
                    'city': birthday.branch.city  # Return the branch city as well
                }# Assuming Birthday has a relationship with Branch
            }
            result.append(birthday_data)

        # Return the result as JSON
    
        return jsonify(result)

    @jwt_required()
    def delete(self):
        # Get the ID from the request arguments
        birthday_id = request.args.get('id')

        if not birthday_id:
            return {'error': 'Missing id parameter'}, 400

        birthday = Birthday.query.get(birthday_id)
        if not birthday:
            return {'error': 'Birthday event not found'}, 404
        
        db.session.delete(birthday)
        db.session.commit()

        return {'message': 'Birthday event deleted successfully'}, 200
    @jwt_required()
    def put(self):
    # Get the ID from the request arguments
     birthday_id = request.args.get('id')
 
     if not birthday_id:
         return {'error': 'Missing id parameter'}, 400

    # Get the JSON data from the request
     data = request.get_json()
     new_name = data.get('name')
     new_date = data.get('date')

     if not new_name and not new_date:
        return {'error': 'Missing name or date in request body'}, 400

    # Find the birthday event by ID
     birthday = Birthday.query.get(birthday_id)
     if not birthday:
        return {'error': 'Birthday event not found'}, 404

    # Update the birthday details
     if new_name:
        birthday.name = new_name
     if new_date:
        birthday.date = new_date
        
     db.session.commit()

     return {'message': 'Birthday updated successfully'}, 200

class EventResource(Resource):
    def post(self):
        data = request.get_json()
        new_event = Event(
            date=data['date'],
            event_description=data['event_description'],
            branch_id=data['branch_id']
        )
        db.session.add(new_event)
        db.session.commit()

        return {'message': 'אירוע נוסף בהצלחה'}, 201
    def get(self):
        # Get the branch_id from the request arguments (if provided)
        branch_id = request.args.get('branch_id')

        # If a branch_id is provided, filter by that branch
        if branch_id:
            events = Event.query.filter_by(branch_id=branch_id).all()
        else:
            events = Event.query.all()

        result = []
        for event in events:
            event_data = {
                'id': event.id,
                'date': event.date,
                'event_description': event.event_description,
                'branch': {
                    'id': event.branch.id,
                    'city': event.branch.city  # Return the branch city as well
                }
            }
            result.append(event_data)

        return jsonify(result)




    @jwt_required()
    def delete(self):
        # Get the ID from the request arguments
        event_id = request.args.get('id')

        if not event_id:
            return {'error': 'Missing id parameter'}, 400

        event = Event.query.get(event_id)
        if not event:
            return {'error': 'Event not found'}, 404
        
        db.session.delete(event)
        db.session.commit()

        return {'message': 'Event deleted successfully'}, 200

    @jwt_required()
    def put(self):
    # Get the ID from the request arguments
     event_id = request.args.get('id')

     if not event_id:
        return {'error': 'Missing id parameter'}, 400

    # Get the JSON data from the request
     data = request.get_json()
     new_description = data.get('event_description')
     new_date = data.get('date')

     if not new_description and not new_date:
        return {'error': 'Missing event_description or date in request body'}, 400

    # Find the event by ID
     event = Event.query.get(event_id)
     if not event:
        return {'error': 'Event not found'}, 404

    # Update the event details
     if new_description:
         event.event_description = new_description
     if new_date:
        event.date = new_date

     db.session.commit()

     return {'message': 'Event updated successfully'}, 200


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            return {'error': 'Invalid username or password'}, 401

        # Create a new token
        access_token = create_access_token(identity=user.id)

        return {'access_token': access_token}, 200
    
class RegisterResource(Resource):
    def post(self):
        print("hey")
        data = request.get_json()
        username = data['username']
        password = data['password']
        print(username)
        # Validate input
        if not username or not password:
            return {'error': 'Username and password are required'}, 400

        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user instance
        new_user = User(username=username, password_hash=hashed_password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201


class BranchResource(Resource):
    
    # Get all branches
    def get(self):
        branches = Branch.query.all()  # Get all branches
        result = []
        for branch in branches:
            branch_data = {
                'id': branch.id,
                'city': branch.city,
                'address': branch.address  # Include address if available
            }
            result.append(branch_data)

        return jsonify(result)

    # Create a new branch
    @jwt_required()
    def post(self):
        data = request.get_json()
        new_branch = Branch(city=data['city'], address=data.get('address'))  # Create new branch with optional address
        db.session.add(new_branch)
        db.session.commit()

        return {'message': 'Branch created successfully'}, 201

    # Delete a branch
    @jwt_required()
    def delete(self):
        branch_id = request.args.get('id')
        if not branch_id:
            return {'error': 'Missing branch id'}, 400
        
        branch = Branch.query.get(branch_id)
        if not branch:
            return {'error': 'Branch not found'}, 404
        
        db.session.delete(branch)
        db.session.commit()

        return {'message': 'Branch deleted successfully'}, 200

    # Update a branch
    @jwt_required()
    def put(self):
        branch_id = request.args.get('id')
        if not branch_id:
            return {'error': 'Missing branch id'}, 400
        
        data = request.get_json()
        branch = Branch.query.get(branch_id)
        if not branch:
            return {'error': 'Branch not found'}, 404
        
        branch.city = data.get('city', branch.city)  # Update city if provided
        branch.address = data.get('address', branch.address)  # Update address if provided
        db.session.commit()

        return {'message': 'Branch updated successfully'}, 200
