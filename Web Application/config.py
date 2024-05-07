from dotenv import load_dotenv
import pyodbc
import os
load_dotenv()

DATABASE_SERVER = os.getenv('SERVER')
DATABASE_NAME = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('USERNAME')
DATABASE_PASSWORD = os.getenv('PASSWORD')

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = F'mssql+pyodbc://{DATABASE_SERVER}/{DATABASE_NAME}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
SQLALCHEMY_TRACK_MODIFICATIONS = False