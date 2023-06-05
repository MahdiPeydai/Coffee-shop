import os
from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')

IMAGE_EXTENSION = os.getenv('IMAGE_EXTENSION')
CATEGORY_IMAGE_FOLDER = os.getenv('CATEGORY_IMAGE_FOLDER')

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB = os.getenv('MYSQL_DB')
