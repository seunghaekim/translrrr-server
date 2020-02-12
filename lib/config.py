import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
ENV = 'development'
SECRET_KEY = os.getenv('SERVER_SECRET_KEY')
KAKAO_APP_KEY = os.getenv('KAKAO_APP_KEY')