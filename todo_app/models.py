from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

def get_ist_time():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

class TodoUser(db.Model):
    __tablename__ = 'todo_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    phone = db.Column(db.String(20))    
    email = db.Column(db.String(120))

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('todo_users.id'))
    created_at = db.Column(db.DateTime, default=get_ist_time)
