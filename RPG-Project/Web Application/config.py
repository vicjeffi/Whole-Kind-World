from dotenv import load_dotenv
# import pyodbc
import os
load_dotenv()

DATABASE_SERVER = os.getenv('SERVER')
DATABASE_NAME = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('USERNAME')
DATABASE_PASSWORD = os.getenv('PASSWORD')

SECRET_KEY = os.getenv('SECRET_KEY')

# /// Connection string

# MS SQL SERVER ON MY PC
# SQLALCHEMY_DATABASE_URI = F'mssql+pyodbc://{DATABASE_SERVER}/{DATABASE_NAME}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

# SERVER MYSQL 
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_SERVER}/{DATABASE_NAME}'

# /// End Connection string

SQLALCHEMY_TRACK_MODIFICATIONS = False

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

MAIL_USERNAME = os.getenv('SMTP_LOGIN')
MAIL_PASSWORD = os.getenv('SMTP_PASSWORD')
MAIL_DEFAULT_SENDER = MAIL_USERNAME