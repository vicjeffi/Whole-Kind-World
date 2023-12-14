# .env file vars import
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_NAME = os.getenv('DATABASE_NAME')

