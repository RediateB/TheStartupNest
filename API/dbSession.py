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
   "postgresql://phase2:Nedamcoacademy2@phase2.postgres.database.azure.com:5432/startupnest_db"
)
Session = sessionmaker(bind=engine)
