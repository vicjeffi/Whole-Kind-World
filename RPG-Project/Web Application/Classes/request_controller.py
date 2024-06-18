from flask import render_template, redirect, url_for, request, session, flash
from Models.user_model import Users
from Models.help_request import HelpRequest
from Classes.auth_controller import login_check
from db_extension import db

import re

from sqlalchemy import desc

word_files = {
    'english': 'BadWordsLib/cursed_eng.txt',
    'russian': 'BadWordsLib/cursed_ru.txt'
}

from BadWordsLib.profanity_filter import ProfanityFilter

# Инициализация фильтра с неприемлемыми словами из файлов
profanity_filter = ProfanityFilter(word_files)

def contains_unacceptable_words(text, word_list):
    text_lower = text.lower()
    for word in word_list:
        if re.search(r'\b' + re.escape(word.lower()) + r'\b', text_lower):
            return True
    return False

def create_request():
    if not login_check():
        session['ErrorMessage'] = 'Вы не вошли в аккаунт!'
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        LoginedUser = session.get('LoginedUser', None)
        user : Users = Users.query.filter_by(Email=LoginedUser['Email']).first()

        if LoginedUser:
            name = request.form['title']
            description = request.form['description']
            file = request.files.get('fileDoc')
            imageFile = request.files.get('fileImg')
            reward = request.form['reward']

            # Проверка на наличие неприемлемых слов
            if (profanity_filter.contains_unacceptable_words(name, 'russian') or
                profanity_filter.contains_unacceptable_words(description, 'russian')):
                session['ErrorMessage'] = 'Название или описание содержит неприемлемые слова!'
                return redirect(url_for('create_request'))

            help_request_id = user.create_help_request(name, description, reward, file, imageFile)
            return redirect(url_for('request', User = LoginedUser, request_id = help_request_id)) 
    else:
        LoginedUser = session.get('LoginedUser', None)
        error_message = session.pop('ErrorMessage', None)
        return render_template('create-event.html', ErrorMessage=error_message, User = LoginedUser)

def help_request(request_id = None):
    if not request_id:
        return redirect(url_for('requests'))
    
    LoginedUser = session.get('LoginedUser', None)
    help_request : HelpRequest = HelpRequest.query.filter(HelpRequest.ID == request_id).first()
    RequestCreator : Users = Users.query.filter(Users.ID == HelpRequest.CreatorID).first()

    return render_template('event.html', User = LoginedUser, HelpRequest = help_request, RequestCreator = RequestCreator)

def help_requests():
    if not login_check():
        session['ErrorMessage'] = 'Вы не вошли в аккаунт!'
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        text = request.form['search']
        return text
    else:
        LoginedUser = session.get('LoginedUser', None)
        # Получаем 3 последние записи, где Reward >= 100
        last_three_high_reward = HelpRequest.query.filter(HelpRequest.Reward >= 100).order_by(desc(HelpRequest.CreationTime)).limit(3).all()

        # Получаем 3 последние записи, где Reward <= 100
        last_three_low_reward = HelpRequest.query.filter(HelpRequest.Reward <= 100).order_by(desc(HelpRequest.CreationTime)).limit(3).all()

        # Получаем 3 самые старые записи, где Status = "Активен"
        three_oldest_active = HelpRequest.query.filter(HelpRequest.Status == "Активен").order_by(HelpRequest.CreationTime).limit(3).all()

        top_three_active_users = Users.query.order_by(desc(Users.Rewards)).limit(3).all()

        return render_template('requests.html', 
                        HighReward = last_three_high_reward, 
                        LowReward = last_three_low_reward, 
                        OldestActive = three_oldest_active, 
                        TopThreeUser = top_three_active_users,
                        User = LoginedUser)
   