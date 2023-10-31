from datetime import datetime
from uuid import uuid4
from random import randint
from flask_login import UserMixin
from sqlalchemy.orm import relationship, Session
from sqlalchemy import (Column, Integer, String, Boolean,
                        DateTime, Enum as PgEnum, ForeignKey, UUID)

from API.core.model.enumTypes import UserTypeEnum, AccountStatus, LoginStatus, AccessLevelAction
from API.dbSession import Base, engine


class AccountModel(Base, UserMixin):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(32), unique=True, nullable=False, default=uuid4().hex)

    username = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    role = Column(PgEnum(UserTypeEnum), nullable=False, default=UserTypeEnum.USER)
    approved = Column(Boolean, default=False, nullable=False)

    alternative_id = Column(String(32), unique=True, nullable=False, default=uuid4().hex)
    first_time_login = Column(Boolean, nullable=False, default=True)
    password_reset_requested = Column(Boolean, nullable=False, default=False)
    account_status = Column(PgEnum(AccountStatus), nullable=False, default=AccountStatus.ACTIVE)
    login_status = Column(PgEnum(LoginStatus), nullable=False, default=LoginStatus.LOGGED_OUT)
    date_of_account_creation = Column(DateTime, nullable=False, default=datetime.now)
    deleted = Column(Boolean, nullable=False, default=False)
    date_of_account_removal = Column(DateTime, nullable=True)

    password_resets = relationship("PasswordReset", back_populates="account", cascade="all, delete-orphan")
    # token = relationship("TokenModel", back_populates="account", cascade="all, delete-orphan")

    def __init__(self, alternative_id, user_id, firstname, lastname, email, role, password, *args, **values):
        super().__init__(*args, **values)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.role = role
        self.password = password
        self.user_id = user_id
        self.alternative_id = alternative_id

    def save(self, session: Session):
        session.add(self)
        session.commit()

    def get_id(self):
        return str(self.alternative_id)

    def change_password(self, new_pass, session):
        # from app import flask_bcrypt
        # self.password = flask_bcrypt.generate_password_hash(new_pass).decode("utf-8")
        self.first_time_login = False
        self.password_reset_requested = False
        self.alternative_id = uuid4().hex
        self.save(session)
        return True

    def password_reset(self, session):
        self.password_reset_requested = True
        self.save(session)
        return True

    def update_account(self, session, username=None, email=None, firstname=None, lastname=None):
        if email is not None:
            self.email = email
        if firstname is not None:
            self.firstname = firstname
        if lastname is not None:
            self.lastname = lastname
        if username is not None:
            self.username = username
        self.save(session)
        return True

    def get_profile(self):
        return {
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "role": self.role.value,
            "approved": self.approved,
        }

    def update_role(self, session, action):
        if action == "upgrade":
            self.role = UserTypeEnum.ADMIN
        elif action == "downgrade":
            self.role = UserTypeEnum.USER
        self.save(session)
        return True


class PasswordReset(Base):
    __tablename__ = "password_reset_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    secret_key = Column(Integer, default=randint(10000000, 99999999), nullable=False)

    account = relationship("AccountModel", back_populates="password_resets")

    def __init__(self, user, *args, **values):
        super().__init__(*args, **values)
        self.user = user

    def save(self, session: Session):
        session.add(self)
        session.commit()

    def remove(self, session: Session):
        session.delete(self)
        session.commit()

    def get_secret_key(self):
        return self.secret_key

    def check_secret_key(self, session, user, secret_key, new_pass):
        if self.user != user:
            return False
        elif self.secret_key != secret_key:
            return False
        try:
            user_obj = self.user
            user_obj.change_password(new_pass)
            self.remove(session)
            return True
        except Exception as e:
            return e


class AccountStatusChangeActivityLogModel(Base):
    __tablename__ = "status_change_log"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    modifier_admin_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    modified_user_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    status_change_from = Column(PgEnum(AccountStatus), nullable=False)
    status_change_to = Column(PgEnum(AccountStatus), nullable=False)
    reason_for_change = Column(String(255), nullable=False)
    date_of_status_modification = Column(DateTime, nullable=False, default=datetime.now)

    modifier_admin = relationship("AccountModel", foreign_keys=[modifier_admin_id])
    modified_user = relationship("AccountModel", foreign_keys=[modified_user_id])


class AuthorizationChangeActivityLogModel(Base):
    __tablename__ = "authorization_change_log"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    modifier_admin_id = Column(String, ForeignKey("accounts.user_id"), nullable=False)
    modified_user_id = Column(String, ForeignKey("accounts.user_id"), nullable=False)
    action_type = Column(PgEnum(AccessLevelAction), nullable=False)
    reason_for_change = Column(String(255), nullable=False)
    date_of_status_modification = Column(DateTime, nullable=False, default=datetime.now)

    modifier_admin = relationship("AccountModel", foreign_keys=[modifier_admin_id])
    modified_user = relationship("AccountModel", foreign_keys=[modified_user_id])

    def __init__(self, admin_id, user_id, action_type, remark, *args, **values):
        super().__init__(*args, **values)
        self.modifier_admin_id = admin_id
        self.modified_user_id = user_id
        self.action_type = AccessLevelAction(action_type)
        self.reason_for_change = remark


Base.metadata.create_all(engine)
