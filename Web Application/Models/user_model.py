from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from Models.help_request import HelpRequest
from Models.users_requests import UsersHelpRequests, UsersCreatedRequests

from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    Surname = db.Column(db.String(255), nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    FatherName = db.Column(db.String(255), nullable=False)

    Email = db.Column(db.String(255), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)

    Sex = db.Column(db.String(10), nullable=True)
    Icon = db.Column(db.LargeBinary(50), nullable=True)
    Description = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        """Устанавливает ХЭШИРОВАННЫЙ пароль для пользователя."""
        self.Password = generate_password_hash(password)

    def hide_secrets(self):
        """Скрывает данные пользователя для всеобщего одозрения.\n
        Используется в случае передачи данных чужого пользователя 
        (соответственно перед передачей)
        """
        self.Password = "Скрыто"
        self.PhoneNumber = "Скрыто"
        self.Email = "Скрыто"

    def check_password(self, password):
        """Проверяет введенный пароль."""
        return check_password_hash(self.Password, password)
    
    def create_help_request(self, name, description, deadlines, status, files=None, img_file=None):
        """Метод для создания запроса помощи пользователем."""
        # Проверка, что пользователь аутентифицирован
        if not self.ID:
            raise ValueError("Вы пытаетесь выдать седя за другого пользователя, либо забыли войти!")
        
        # Создание нового запроса помощи
        new_help_request = HelpRequest(
            Name=name,
            Description=description,
            CreationTime=datetime.now(),
            Deadlines=deadlines,
            Status=status,
            Files=files,
            ImgFIle=img_file
        )
        
        # Сохранение запроса помощи в базу данных
        db.session.add(new_help_request)
        db.session.commit()
        
        # Связывание пользователя с созданным запросом помощи
        new_user_help_request = UsersCreatedRequests(
            UserID=self.ID,
            HelpRequestID=new_help_request.ID
        )
        
        # Сохранение связи пользователя и запроса помощи в базу данных
        db.session.add(new_user_help_request)
        db.session.commit()
    
    def created_help_requests(self):
        """Возвращает список всех созданных пользователем запросов о помощи."""
        created_requests = UsersCreatedRequests.query.filter_by(UserID=self.ID).all()

        help_request_ids = [request.HelpRequestID for request in created_requests]
        help_requests = HelpRequest.query.filter(HelpRequest.ID.in_(help_request_ids)).all()

        return help_requests