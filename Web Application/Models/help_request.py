from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta
from markupsafe import Markup

db = SQLAlchemy()

class HelpRequest(db.Model):
    __tablename__ = 'HelpRequests'

    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String, nullable=True)
    CreationTime = db.Column(db.DateTime, nullable=False) # В последствии форматируемый шаблоном ниже
    Deadlines = db.Column(db.DateTime, nullable=True)
    Status = db.Column(db.String(50), nullable=False)
    Files = db.Column(db.Binary(50), nullable=True)
    ImgFIle = db.Column(db.Binary(50), nullable=True)
    Reward = db.Column(db.Integer, nullable=False)

# Шаблон формата:
# если прошло больше чем день: 'x дней и y часов назад'
# если прошло меньше чем 1 день, но больше чем 1 час: 'y часов назад'
# если прошло меньше чем 1 день, и меньше чем 1 час, и больше чем 1 минута: 'b минут назад'
# если прошло меньше чем 1 день, и меньше чем 1 час, и меньше чем 1 минута: 'c секунд назад'
def format_time_since(published_time):
    now = datetime.now()
    delta = now - published_time

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return Markup(f"{days} {'дней' if days > 1 else 'день'} и {hours} {'часов' if hours > 1 else 'час'} назад")
    elif hours > 0:
        return Markup(f"{hours} {'часов' if hours > 1 else 'час'} назад")
    elif minutes > 0:
        return Markup(f"{minutes} {'минут' if minutes > 1 else 'минута'} назад")
    else:
        return Markup(f"{seconds} {'секунд' if seconds > 1 else 'секунда'} назад")