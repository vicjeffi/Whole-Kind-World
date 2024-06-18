from flask import Flask, render_template
from flask_session import Session
from db_extension import db
from Models.error import error404

application = Flask(__name__)

# Загрузка конфигурации из файла
application.config.from_pyfile('config.py')

# Инициализация секретного ключа
application.secret_key = application.config['SECRET_KEY']

# Настройка сессии
application.config['SESSION_TYPE'] = 'filesystem'
Session(application)

# Подключение БД
db.init_app(application)

# Импортирование модулей роутов
from Classes.auth_controller import try_registration, try_login, unlogin, verify_email
from Classes.profile_controller import profile, profile_edit
from Classes.index_controller import index
from Classes.message_controller import get_messages
from Classes.request_controller import create_request, help_request, help_requests
from jinja_filters import format_time_since, truncate_filter, jpeg_image, b64encode_filter

# Объявляю роуты
application.add_url_rule('/registration', 'registration', try_registration, methods=['GET', 'POST'])
application.add_url_rule('/verify-email/<string:token>', 'verify-email', verify_email)
application.add_url_rule('/login', 'login', try_login, methods=['GET', 'POST'])
application.add_url_rule('/unlogin', 'unlogin', unlogin)
application.add_url_rule('/profile/<int:user_id>', 'profile', profile)
application.add_url_rule('/profile-edit', 'profile-edit', profile_edit, methods=['GET', 'POST'])
application.add_url_rule('/messages', 'messages', get_messages, methods=['GET'])
application.add_url_rule('/create-request', 'create-request', create_request, methods=['GET', 'POST'])
application.add_url_rule('/request/<int:request_id>', 'request', help_request)
application.add_url_rule('/requests', 'requests', help_requests)
application.add_url_rule('/', 'index', index)

# Загрузка всех шалонов данных для Jinja
application.jinja_env.filters['format_time_since'] = format_time_since
application.jinja_env.filters['truncate'] = truncate_filter
application.jinja_env.filters['jpeg_image'] = jpeg_image
application.jinja_env.filters['b64encode'] = b64encode_filter

# Ловим ошибки
@application.errorhandler(404)
def not_found(e):
    return render_template("oops-error.html", Error=error404)

@application.route("/test")
def hello():
   return "<h1 style='color:blue'>Hello There!</h1>"

# Запуск приложения
if __name__ == "__main__":
    with application.app_context():
        db.create_all()

    application.run(host='0.0.0.0', debug=True)