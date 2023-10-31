from datetime import datetime
from uuid import uuid4
from random import randint
from sqlalchemy.orm import relationship, Session
from sqlalchemy import (Column, Integer, String, Boolean,
                        DateTime, Enum as PgEnum, ForeignKey, UUID)

from API.dbSession import Base, engine
from API.core.model.enumTypes import QuestionCategory


class Stem(Base):
    __tablename__ = "question_stems"

    id = Column(Integer, primary_key=True)
    questionStems = Column(String, nullable=False)
    question = relationship("Question",
                            back_populates="question_stem",
                            uselist=False)


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    answer = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    question = relationship("Question", back_populates="alternatives")


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    category = Column(PgEnum(QuestionCategory), nullable=False)
    stem = Column(Integer, ForeignKey('question_stems.id'), nullable=False)

    question_stem = relationship("Stem",
                                 back_populates="question",
                                 cascade="all, delete-orphan",
                                 single_parent=True,
                                 uselist=False)
    alternatives = relationship("Answer",
                                back_populates="question",
                                cascade="all, delete-orphan",
                                single_parent=True)


class ConsultantAnswerRecord(Base):
    __tablename__ = "consultant_answer_record"
    id = Column(Integer, primary_key=True)

    consultant = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    answer_id = Column(Integer, ForeignKey('answer.id'), nullable=False)


class ClientAnswerRecord(Base):
    __tablename__ = "client_answer_record"
    id = Column(Integer, primary_key=True)

    client = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    answer_id = Column(Integer, ForeignKey('answer.id'), nullable=False)


Base.metadata.create_all(engine)
