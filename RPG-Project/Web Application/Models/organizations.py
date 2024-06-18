from flask_sqlalchemy import SQLAlchemy
from db_extension import db

class Organization(db.Model):
    __tablename__ = 'Organizations'

    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    ContactInfo = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String, nullable=True)