# Flask stuff
from flask import Flask, render_template, request, redirect, url_for, flash
# To HASH things
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py') # go to config.py and .env file with vars
app.secret_key = app.config['SECRET_KEY']

app.app_context().push()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Хеширование пароля
        hashed_password = generate_password_hash(password, method='sha256')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Добавление пользователя в базу данных
        cursor.execute('INSERT INTO User (username, password) VALUES (?, ?)',
                       (username, hashed_password))

        conn.commit()
        conn.close()

        flash('Регистрация успешна', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Получение данных пользователя из базы данных
        cursor.execute('SELECT * FROM User WHERE username = ?', (username,))
        user = cursor.fetchone()

        conn.close()

        # Проверка пароля
        if user and check_password_hash(user['password'], password):
            flash('Вход выполнен успешно', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

    