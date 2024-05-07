from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UsersHelpRequests(db.Model):
    __tablename__ = 'UsersHelpRequests'

    UserID = db.Column(db.Integer, primary_key=True)
    HelpRequestID = db.Column(db.Integer, primary_key=True)

class UsersCreatedRequests(db.Model):
    __tablename__ = 'UsersCreatedRequests'

    UserID = db.Column(db.Integer, primary_key=True)
    HelpRequestID = db.Column(db.Integer, primary_key=True)