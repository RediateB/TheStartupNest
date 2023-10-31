from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.session_protection = 'strong'
sql_db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()
