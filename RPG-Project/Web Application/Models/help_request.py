from flask_sqlalchemy import SQLAlchemy
from db_extension import db


class HelpRequest(db.Model):
    __tablename__ = 'HelpRequests'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String, nullable=True)
    CreationTime = db.Column(db.DateTime, nullable=False) # В последствии форматируемый шаблоном ниже
    Status = db.Column(db.String(50), nullable=False)
    Files = db.Column(db.LargeBinary, nullable=True)
    ImgFIle = db.Column(db.VARBINARY('MAX'), nullable=True)
    Reward = db.Column(db.Integer, nullable=False)
    CreatorID = db.Column(db.Integer, db.ForeignKey('Users.ID'), nullable=False)

# Шаблон формата:
# если прошло больше чем день: 'x дней и y часов назад'
# если прошло меньше чем 1 день, но больше чем 1 час: 'y часов назад'
# если прошло меньше чем 1 день, и меньше чем 1 час, и больше чем 1 минута: 'b минут назад'
# если прошло меньше чем 1 день, и меньше чем 1 час, и меньше чем 1 минута: 'c секунд назад'