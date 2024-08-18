from flask_restful import Resource
from models import Birthday, db,Event  # Import your Birthday model and db instance
from flask import jsonify, request

class BirthDayResource(Resource):
    def post(self):
        data = request.get_json()  # Get the JSON data from the request
        new_birthday = Birthday(name=data['name'], date=data['date'])  # Create a new Birthday instance
        db.session.add(new_birthday)  # Add the new birthday to the session
        db.session.commit()  # Commit the session to the database
        
        return {'message': 'יום הולדת נוסף בהצלחה'}, 201  # Return a success message
    
    def get(self):
        users = Birthday.query.all()  # Query all birthdays from the database
        result = []
        for user in users:
            user_data = {
                'id': user.id,
                'date': user.date,
                'name': user.name
            }
            result.append(user_data)
        return jsonify(result)  
    def delete(self):
        # Get the ID from the request arguments
        event_id = request.args.get('id')

        if not event_id:
            return {'error': 'Missing id parameter'}, 400

        event = Birthday.query.get(event_id)
        if not event:
            return {'error': 'Event not found'}, 404
        
        db.session.delete(event)
        db.session.commit()
    # Return the list of all birthdays as JSON
class EventResource(Resource):
    def post(self):
        # Get the JSON data from the request
        data = request.get_json()

        # Create a new Event instance
        new_event = Event(date=data['date'], event_description=data['event_description'])

        # Add the new event to the session and commit to the database
        db.session.add(new_event)
        db.session.commit()

        # Return a success message
        return {'message': 'אירוע נוסף בהצלחה'}, 201
    
    def get(self):
        # Query all events from the database
        events = Event.query.all()
        result = []
        for event in events:
            event_data = {
                'id': event.id,
                'date': event.date,
                'event_description': event.event_description
            }
            result.append(event_data)

        # Return the list of all events as JSON
        return jsonify(result)
    
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