from datetime import datetime
from sqlalchemy.orm import relationship, Session
from sqlalchemy import (Column, Integer, String, Boolean,
                        DateTime, Enum as PgEnum, ForeignKey,
                        Date, Time)

from API.dbSession import Base, engine
from API.core.model.enumTypes import MeetingType


class ConsultantClientPair(Base):
    __tablename__ = "consultant_client_pair"

    id = Column(Integer, primary_key=True)
    consultant = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    client = Column(Integer, ForeignKey('accounts.id'), nullable=False)


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True)
    consultant = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    client = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    meeting_type = Column(PgEnum(MeetingType), nullable=False)
    booked = Column(Boolean, default=False, nullable=True)
    canceled = Column(Boolean, default=False, nullable=True)
    cancellation_reason = Column(String, default=None, nullable=True)


Base.metadata.create_all(engine)
