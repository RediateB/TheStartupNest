import os
from datetime import timedelta

import flask

flask.cli.load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CORS_HEADERS = "Content-Type"
    # SESSION_COOKIE_SECURE = True
    # SESSION_COOKIE_SAMESITE = 'None'
    SQLALCHEMY_DATABASE_URI = " postgresql://phase2:Nedamcoacademy2@phase2. postgres. database. azure.com:5432/startupnest_db"


