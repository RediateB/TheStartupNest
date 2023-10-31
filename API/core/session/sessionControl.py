from flask_login import login_user, logout_user, current_user

from API.core.model.enumTypes import AccountStatus, LoginStatus
from API.core.model.helperUtils import InvalidUserInput
from API.dbSession import Session
from API.core.model.databaseModel import AccountModel, PasswordReset


class SessionControl:
    @staticmethod
    def signin_user(incoming_data):
        from app import flask_bcrypt
        try:
            with Session() as session:
                username = incoming_data.get("username")
                password = incoming_data.get("password")
                remember_me = incoming_data.get("remember_me")
                if not remember_me:
                    remember_me = False
                remember_me = True if remember_me == "true" else False
                if not username or not password:
                    raise InvalidUserInput(message="Required fields are missing!")

                user = session.query(AccountModel).filter(AccountModel.email == username).first()
                if not user:
                    raise InvalidUserInput(message="Invalid Credentials")
                if user.account_status != AccountStatus.ACTIVE:
                    raise InvalidUserInput(
                        message="Your account is blocked! Please contact your system administrator")
                if user.password_reset_requested:
                    reset_request = session.query(PasswordReset).filter(PasswordReset.user == user.id).first()
                    if (reset_request.secret_key == password or
                            flask_bcrypt.check_password_hash(user.password, password)):
                        authenticated = True
                        login_type = 1
                    else:
                        raise InvalidUserInput(message="Invalid Credentials")
                elif flask_bcrypt.check_password_hash(user.password, password):
                    authenticated = True
                    login_type = 2 if user.first_time_login else 0
                else:
                    raise InvalidUserInput(message="Invalid Credentials")

                if authenticated:
                    user.login_status = LoginStatus.LOGGED_IN
                    login_user(user, remember=remember_me)
                    session.commit()
                    return {"result": {"login_type": login_type}}, 200
            raise InvalidUserInput(message="Invalid Credentials")
        except InvalidUserInput as err:
            print(err.message)
            return {"error": err.message}, 500
        except Exception:
            raise

    @staticmethod
    def sign_out_user():
        try:
            with Session() as session:
                user_id = current_user.alternative_id
                user = session.query(AccountModel).filter(AccountModel.alternative_id == user_id).first()

                user.login_status = LoginStatus.LOGGED_OUT
                session.commit()
            logout_user()
            return {"result": "logged out"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

