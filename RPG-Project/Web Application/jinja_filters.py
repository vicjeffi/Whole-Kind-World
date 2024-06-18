from markupsafe import Markup
from datetime import datetime
import base64

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
    

def truncate_filter(s, length=13):
    if len(s) <= length:
        return s
    else:
        return s[:length] + "..."
    
def jpeg_image(image):
    if image:
        return base64.b64encode(image).decode('utf-8')
    else:
        return None
    
def b64encode_filter(data):
    if data is None:
        return ""
    return Markup(base64.b64encode(data).decode('utf-8'))