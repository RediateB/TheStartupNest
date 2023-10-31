import os

import flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

flask.cli.load_dotenv()

ssl_mode = 'require'

# create engine and session
engine = create_engine(
    f"postgresql://{os.environ.get('DATABASE_USERNAME')}:"
    f"{os.environ.get('DATABASE_PASSWORD')}@{os.environ.get('DATABASE_HOST')}:"
    f"{os.environ.get('DATABASE_PORT')}/{os.environ.get('APP_DATABASE')}",
    connect_args={"sslmode": "disable"}
)
Session = sessionmaker(bind=engine)
