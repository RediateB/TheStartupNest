from datetime import datetime
from uuid import uuid4
from random import randint
from flask_login import UserMixin
from sqlalchemy.orm import relationship, Session
from sqlalchemy import (Column, Integer, String, Boolean,
                        DateTime, Enum as PgEnum, ForeignKey, UUID)

from API.dbSession import Base, engine


class ConsultantDocumentModel(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    document = Column(String, nullable=False)
