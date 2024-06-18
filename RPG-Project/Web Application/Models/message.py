from db_extension import db

class Message(db.Model):
    __tablename__ = 'Message'

    Id = db.Column(db.Integer, primary_key=True)
    ReceiverID = db.Column(db.Integer, db.ForeignKey('Users.ID'))
    Text = db.Column(db.String(255))
    Timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())