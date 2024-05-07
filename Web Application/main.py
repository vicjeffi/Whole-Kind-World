from flask import Flask, render_template, session
from flask_session import Session

from Classes.auth_controller import registration, login, unlogin
from Classes.profile_controller import profile, profile_edit
from Classes.index_controller import index

from Models.user_model import db
from Models.error import error404

# Макеты Jinjs
from Models.help_request import format_time_since

app = Flask(__name__)

# Загрузка конфигурации из файла
app.config.from_pyfile('config.py')

# Инициализация секретного ключа
app.secret_key = app.config['SECRET_KEY']

# Настройка сессии
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Подключение БД
db.init_app(app)

# Подлючение БД используя ключи из конфига и моделли из папки Models
with app.app_context():
    db.create_all()

# Установка маршрутов для контроллеров
app.add_url_rule('/registration', 'registration', registration, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/profile/<int:user_id>', 'profile', profile)
app.add_url_rule('/profile-edit', 'profile-edit', profile_edit)
app.add_url_rule('/unlogin', 'unlogin', unlogin)
app.add_url_rule('/', 'index', index)

# Загрузка всех шалонов данных для Jinja
app.jinja_env.filters['format_time_since'] = format_time_since

# Ловим ошибки
@app.errorhandler(404)
def not_found(e):
  return render_template("oops-error.html", Error = error404) 

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, port=80)

## Миша! Когда будешь переносить сервер надо будет менять все:

# Настройка App Service: Создайте App Service в своей подписке Azure через портал Azure.
# Настройка окружения: В разделе настройки вашего App Service перейдите в раздел "Настройки приложения" и настройте переменные среды и другие параметры вашего приложения.
# Деплоймент приложения: Деплойте ваше Flask-приложение на App Service. Вам может понадобиться использовать Git, Docker, FTP или другие методы, поддерживаемые Azure, для деплоймента вашего кода.
# Конфигурация файлов: Убедитесь, что файлы конфигурации, такие как config.py, находятся в соответствующих местах и правильно настроены для работы на сервере Azure.
# Настройка порта: Вам не нужно указывать порт 80 в вашем приложении, так как Azure автоматически привязывает ваше приложение к соответствующему порту.

## !!! https://letsencrypt.org/ru/getting-started/ для сертификации https подключения !!!