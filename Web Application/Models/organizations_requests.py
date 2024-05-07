from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OrganizationsHelpRequests(db.Model):
    __tablename__ = 'OrganizationsHelpRequests'
    OrganizationID = db.Column(db.Integer, primary_key=True)
    HelpRequestID = db.Column(db.Integer, primary_key=True)

class OrganizationsCreatedRequests(db.Model):
    __tablename__ = 'OrganizationsCreatedRequests'
    OrganizationID = db.Column(db.Integer, primary_key=True)
    HelpRequestID = db.Column(db.Integer, primary_key=True)