from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Birthday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    

    def __repr__(self):
        return f'<Birthday {self.date} {self.name} >'
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80), nullable=False)
    event_description= db.Column(db.String(80), nullable=False)
      # New field to mark non-working days

    

    def __repr__(self):
        return f'<Event {self.date} {self.event_description} >'
