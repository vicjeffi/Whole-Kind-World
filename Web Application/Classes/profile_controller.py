from flask import render_template, session, redirect, url_for, request
from Models.user_model import Users
from Classes.auth_controller import login_check
import base64
    
def profile(user_id=None):
    """
    Отображает профиль пользователя со всеми его данными \n
    В случае если указан user_id, ищет такого пользователя и показывает его профиль
    """
    if user_id:
        # Если это ссылка на профиль другого пользователя
        user_profile = Users.query.filter(Users.ID == user_id).first()
        if user_profile:
            user_profile.hide_secrets()
            if login_check():
                LoginedUser = session['LoginedUser']
                return render_template('profile.html', ProfileUser=user_profile, User=LoginedUser, ElsesProfile=True)
            else:
                return render_template('profile.html', ProfileUser=user_profile, ElsesProfile=True)
        else:
            # Обработка случая, когда профиль не найден
            return render_template('profile_not_found.html')
    else:
        # Если профиль текущего пользователя
        if login_check():
            LoginedUser = session['LoginedUser']
            return render_template('profile.html', ProfileUser=LoginedUser, User=LoginedUser, ElsesProfile=False)
        else:
            # Перенаправляем на страницу входа, если пользователь не аутентифицирован
            session['ErrorMessage'] = "Вы забыли войти в аккаунт!"
            return redirect(url_for('login'))
        
def profile_edit():
    pass