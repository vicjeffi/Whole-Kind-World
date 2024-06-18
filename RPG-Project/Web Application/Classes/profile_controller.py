from flask import render_template, session, redirect, url_for, request
from Models.user_model import Users
from Models.error import error408
from Classes.auth_controller import login_check
    
def profile(user_id=None):
    """
    Отображает профиль пользователя со всеми его данными \n
    В случае если указан user_id, ищет такого пользователя и показывает его профиль
    """
    if user_id:
        # Если это ссылка на профиль другого пользователя
        user_profile : Users = Users.query.filter(Users.ID == user_id).first()
        if user_profile:
            user_profile.hide_secrets()
            CreatedRequests = user_profile.created_help_requests()
            if login_check():
                LoginedUser = session['LoginedUser']
                if LoginedUser['ID'] == user_profile.ID:
                    return render_template('profile.html', ProfileUser=user_profile, User=LoginedUser, MyProfile=True, CreatedRequests = CreatedRequests)
                else:
                    return render_template('profile.html', ProfileUser=user_profile, User=LoginedUser, MyProfile=False, CreatedRequests = CreatedRequests)
            else:
                return render_template('profile.html', ProfileUser=user_profile, MyProfile=False, CreatedRequests = CreatedRequests)
        else:
            # Обработка случая, когда профиль не найден
            return redirect(url_for("oops-error.html", Error = error408))
        
def profile_edit():
    pass