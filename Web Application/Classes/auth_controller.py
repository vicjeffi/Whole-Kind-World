from flask import render_template, redirect, url_for, request, session, flash
from Models.user_model import db, Users
from flask_session import Session
from datetime import datetime

import re

def registration():
    if request.method == 'POST':
        # Получаем данные из формы
        surname = request.form.get('surname')
        name = request.form.get('name')
        father_name = request.form.get('father_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        sex = request.form.get('sex')

        # Проверяем заполнены ли все обязательные поля
        required_fields = {'surname': 'фамилия', 'name': 'имя', 'father_name': 'отчество', 'email': 'адрес электронной почты', 'phone_number': 'номер телефона', 'password': 'пароль', 'sex': 'пол'}
        for field, field_name in required_fields.items():
            if not request.form.get(field):
                return render_template('registration.html', ErrorMessage=f"Не заполнено {field_name}")

        # Проверка корректности электронной почты
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template('registration.html', ErrorMessage="Некорректный адрес электронной почты")
        
        # Проверка уникальности адреса электронной почты
        if Users.query.filter_by(Email=email).first():
            return render_template('registration.html', ErrorMessage="Аккаунт с этой почтой уже существует!")

        # Проверка корректности номера телефона
        if not re.match(r"(\+7|8)\d{10}", phone_number):
            return render_template('registration.html', ErrorMessage="Некорректный номер телефона")

        # Проверка совпадения паролей
        if password != repassword:
            return render_template('registration.html', ErrorMessage="Пароли должны совпадать")

        # Проверка пароля на допустимые символы и длину
        if not re.match(r"^[a-zA-Z0-9!@#$%^&*№%?*-=_+)]+$", password):
            return render_template('registration.html', ErrorMessage="Пароль должен содержать только цифры, символы (кроме кавычек) и латинские буквы")
        if len(password) < 9:
            return render_template('registration.html', ErrorMessage="Пароль должен содержать не менее 9 символов")

        # Создание нового пользователя
        new_user = Users(Surname=surname, Name=name, FatherName=father_name, PhoneNumber=phone_number, Email=email, Sex=sex)
        new_user.set_password(password)

        # Сохранение пользователя в базу данных
        db.session.add(new_user)
        db.session.commit()

        # Перенаправление на страницу входа с сообщением об успешной регистрации
        return redirect(url_for('login', ErrorMessage="Аккаунт создан, вы можете теперь войти и настроить профиль!"))

    # Если запрос не POST, просто отображаем форму регистрации
    start_date = datetime.now().strftime("%Y-%m-%d")
    return render_template('registration.html', StartDate=start_date)

def login():
    # Проверяем зашел ли уже пользователь
    if login_check():
        return redirect(url_for('profile'))
    
    # В случае если пользователь еще не зашел и уже указанны данные формы
    if request.method == 'POST':
        # Получаем данные из формы
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверяем, существует ли пользователь с таким email...
        user = Users.query.filter_by(Email=email).first()
        #  ...и введенный пароль верен
        if user and user.check_password(password):
            # Создаем объект пользователя для сеанса
            session['logged'] = True
            session['LoginedUser'] = {
                'ID': user.ID,
                'Surname': user.Surname,
                'Name': user.Name,
                'FatherName': user.FatherName,
                'PhoneNumber': user.PhoneNumber,
                'Email': user.Email,
                'Sex': user.Sex
            }

            return redirect(url_for('profile'))
        
        else:
            return render_template('login.html', ErrorMessage="Неверный логин или пароль!")
        
    # Если пользователь первый раз зашел на страницу
    # Делаем проверку на наличие сообщений из других методов, например после отправки из unlogin()
    ErrorMessage = session.pop('ErrorMessage', None)
    return render_template('login.html', ErrorMessage=ErrorMessage)

def unlogin():
    # Если пользователь уже вошел в систему, очищаем сессию и перенаправляем на страницу входа
    if login_check():
        session.clear()
        message = "Вы успешно вышли из аккаунта"
    else:
        # Если пользователь уже вышел из аккаунта, просто перенаправляем на страницу входа
        message = "Вы уже вышли из аккаунта"
    
    # Устанавливаем сообщение в сессию
    session['ErrorMessage'] = message
    
    return redirect(url_for('login'))

def login_check():
    """Метод для БЕЗОПАСНОЙ ПРОВЕРКИ СЕАНСА входа пользователя!!! \n
    Только уже после него можно использовать session[''] без крашей \n
    Здесь используется session.get для проверки значения
    """
    logged = session.get('logged')
    user = session.get('LoginedUser')
    
    if logged == True and user:
        return True
    else:
        return False