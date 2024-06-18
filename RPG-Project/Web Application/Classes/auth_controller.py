from flask import render_template, redirect, url_for, request, session, flash, current_app
from Models.user_model import Users
from flask_session import Session
from datetime import datetime
import secrets

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from db_extension import db
# from main import mail

import re
import smtplib

def try_registration():
    """
    Метод обрабатывает попытку регистрации пользователя. \n
    Если запрос является POST запросом, то производится валидация введенных данных и регистрация пользователя,
    иначе отображается страница регистрации.
    """
    if request.method == 'POST':
        surname = request.form.get('surname')
        name = request.form.get('name')
        father_name = request.form.get('father_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        sex = request.form.get('sex')

        error_message = registration_validation(surname, name, father_name, email, phone_number, password, repassword, sex)
        if error_message:
            return render_template('registration.html', ErrorMessage=error_message)

        return registration(surname, name, father_name, email, phone_number, password, sex)
    else:
        start_date = datetime.now().strftime("%Y-%m-%d")
        return render_template('registration.html', StartDate=start_date)

def registration(surname, name, father_name, email, phone_number, password, sex):
    """
    Метод производит регистрацию пользователя на основе переданных данных и сохраняет его в базу данных. \n
    Отдельно вызывает метод для отправки письма с подтвердждением почты
    """
    token = generate_confirmation_key()
    
    send_confirmation_email(email, token)

    new_user = Users(Surname=surname, Name=name, FatherName=father_name, PhoneNumber=phone_number, Email=email, Sex=sex, EmailConfirmed=False, RegistrationToken = token)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    session['ErrorMessage'] ="Теперь осталось подтвердить вашу почту\nВам должно прийти письмо с ссылкой"
    return redirect(url_for('login'))

def generate_confirmation_key():
    return secrets.token_urlsafe(16)

def send_confirmation_email(user_email, key):

    smtp_server = current_app.config['SMTP_SERVER']
    smtp_port = current_app.config['SMTP_PORT']
    smtp_login = current_app.config['SMTP_LOGIN']
    smtp_password = current_app.config['SMTP_PASSWORD']

    # Генерация ссылки для подтверждения
    confirm_url = url_for('verify-email', token=key, _external=True)
    
    html = render_template('email_confirmation.html', confirm_url=confirm_url)
    
    FROM = "monahovmm17@gmail.com"
    TO = user_email
    TEXT = MIMEText(html, "html", "utf-8")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Подтверждение адреса почты"
    msg.attach(TEXT)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(smtp_login, smtp_password)
    server.sendmail(FROM, TO, msg.as_string())
    server.close()

def registration_validation(surname, name, father_name, email, phone_number, password, repassword, sex):
    """
    Метод проверяет введенные данные на корректность и валидность.
    """
    required_fields = {'surname': 'фамилия', 'name': 'имя', 'father_name': 'отчество', 'email': 'адрес электронной почты', 'phone_number': 'номер телефона', 'password': 'пароль', 'sex': 'пол'}
    for field, field_name in required_fields.items():
        if not locals()[field]:
            return f"Не заполнено {field_name}"

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Некорректный адрес электронной почты"
    
    if Users.query.filter_by(Email=email).first():
        return "Аккаунт с этой почтой уже существует!"

    if not re.match(r"(\+7|8)\d{10}", phone_number):
        return "Некорректный номер телефона"

    if password != repassword:
        return "Пароли должны совпадать"

    if not re.match(r"^[a-zA-Z0-9!@#$%^&*№%?*-=_+)]+$", password):
        return "Пароль должен содержать только цифры, символы (кроме кавычек) и латинские буквы"
    
    if len(password) < 9:
        return "Пароль должен содержать не менее 9 символов"

    return None

def try_login():
    """
    Метод обрабатывает попытку входа пользователя в систему. \n
    Если пользователь уже вошел в систему, он перенаправляется на свой профиль.
    Если запрос является POST запросом, происходит попытка входа в систему.
    Если пользователь еще не вошел в систему и данные формы не были отправлены, отображается страница входа.
    """
    if login_check():
        user = session['LoginedUser']
        user_id = user['ID']
        return redirect(url_for('profile', user_id=user_id))
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return login(email, password)
    else:
        error_message = session.pop('ErrorMessage', None)
        return render_template('login.html', ErrorMessage=error_message)

def login(email, password):
    """
    Метод производит попытку входа пользователя в систему на основе данных из формы.
    """
    user : Users = Users.query.filter_by(Email=email).first()
    
    if user and user.check_password(password) and user.EmailConfirmed:
        session['logged'] = True
        session['LoginedUser'] = {
            'ID': user.ID,
            'Surname': user.Surname,
            'Name': user.Name,
            'FatherName': user.FatherName,
            'PhoneNumber': user.PhoneNumber,
            'Email': user.Email,
            'Sex': user.Sex,
            'EmailConfirmed': user.EmailConfirmed
        }
        user_id = user.ID
        return redirect(url_for('profile', user_id=user_id))
    else:
        error_message = "Неверный логин или пароль!"
        return render_template('login.html', ErrorMessage=error_message)

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

def submit_registration(token):
    user : Users = Users.query.filter_by(RegistrationToken=token).first()

    if user:
        user.EmailConfirmed = True
        db.session.commit()
        
        session['ErrorMessage'] = 'Ваш адрес электронной почты успешно подтвержден. Теперь вы можете войти в свой аккаунт.'
        login(user.Email, user.Password)
    else:
        session['ErrorMessage'] =  'Неверный токен регистрации. Пожалуйста, проверьте ссылку и попробуйте снова.'
        return redirect(url_for('login'))
    
def verify_email(token):
    user = Users.query.filter_by(RegistrationToken=token).first()
    if user:
        if user.EmailConfirmed:
            session['ErrorMessage'] = 'Вы уже подтвержили аккаунт, вы можете войти'
            return redirect(url_for('login'))
        else:
            user.EmailConfirmed = True
            user.RegistrationToken = None
            db.session.commit()
            session['ErrorMessage'] = 'Вы подтвердили аккаунт, можете теперь войти'
            return redirect(url_for('login')) 
    else:
        session['ErrorMessage'] = 'Токен устарел, обратитесь в поддержку'
        return redirect(url_for('register')) 