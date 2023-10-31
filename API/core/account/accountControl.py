import uuid
from datetime import datetime
from flask_login import current_user, logout_user
from API.core.model.databaseModel import AccountModel, PasswordReset
from API.core.model.enumTypes import UserTypeEnum
from API.core.model.helperUtils import InvalidUserInput, Validation
from API.dbSession import Session


class AccountControl:
    @staticmethod
    def create_account(incoming_data, role):
        from app import flask_bcrypt
        try:
            if "firstName" not in incoming_data or len(incoming_data["firstName"]) <= 2:
                raise InvalidUserInput(message="Invalid First name")
            if "lastName" not in incoming_data or len(incoming_data["lastName"]) <= 2:
                raise InvalidUserInput(message="Invalid Last name")
            if "username" not in incoming_data or not Validation.validate_username(incoming_data["username"]):
                raise InvalidUserInput(message="Invalid Email Address")
            if "email" not in incoming_data or not Validation.validate_email(incoming_data["email"]):
                raise InvalidUserInput(message="Invalid Email Address")
            if "password" not in incoming_data or not Validation.validate_password(incoming_data["password"]):
                raise InvalidUserInput(message="Invalid Password! Password must be longer than 8 characters, "
                                               "have a capital letter, small letter, and special character")

            with Session() as session:
                approved = True if role == UserTypeEnum.USER else False
                new_result = AccountModel(
                    username=incoming_data["username"],
                    firstname=incoming_data["firstName"],
                    lastname=incoming_data["lastName"],
                    email=incoming_data["email"],
                    password=flask_bcrypt.generate_password_hash(incoming_data["password"]).decode("utf-8"),
                    role=role,
                    approved=approved,
                    user_id=uuid.uuid4().hex,
                    alternative_id=uuid.uuid4().hex
                )
                session.add(new_result)
                session.commit()

            return {'result': "Account created successfully"}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def update_details( incoming_data):
        try:
            with Session() as session:
                user = session.query(AccountModel).filter(
                    AccountModel.alternative_id == current_user.alternative_id).first()

                email = incoming_data.get("email", None)
                firstname = incoming_data.get("firstname", None)
                lastname = incoming_data.get("lastname", None)
                username = incoming_data.get("username", None)

                if user:
                    result = user.update_account(
                        session=session,
                        username=username,
                        firstname=firstname,
                        lastname=lastname
                    )
                    if result:
                        return {"result": "Account update successfully"}, 200
                raise InvalidUserInput(message="Account Not Found")
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def update_password(incoming_data):
        from app import flask_bcrypt
        try:
            with Session() as session:
                user = session.query(AccountModel).filter(
                    AccountModel.alternative_id == current_user.alternative_id).first()

                current_pass = incoming_data.get("current_pass")
                new_pass = incoming_data.get("new_pass")
                new_pass_2 = incoming_data.get("new_pass_2")
                if not current_pass:
                    raise InvalidUserInput(message="Current password is required")
                elif not new_pass or not Validation.validate_password(incoming_password=new_pass):
                    raise InvalidUserInput(message="Invalid Password! Password must longer than 8 characters, "
                                                   "have Capital letter, small letter, and special character")
                elif not new_pass_2:
                    raise InvalidUserInput(message="Re-password is required")
                elif new_pass != new_pass_2:
                    raise InvalidUserInput(message="Invalid Password! New password must match")
                else:
                    reset_request = session.query(PasswordReset).filter(PasswordReset.user == user.id).first()

                    if reset_request and reset_request.check_secret_key(session, user.id, current_pass, new_pass):
                        session.delete(reset_request)
                        return {"result": "`Password updated`"}, 200
                    elif flask_bcrypt.check_password_hash(user.password, current_pass):
                        if reset_request:
                            session.delete(reset_request)
                        session.commit()
                        user.change_password(new_pass, session)
                        session.commit()
                        logout_user()
                        return {"result": "Password updated"}, 200
                    else:
                        raise InvalidUserInput(message="Invalid current password")
        except InvalidUserInput as error:
            return {"error": error.message}, 400
        except Exception as e:
            raise

    @staticmethod
    def get_account():
        try:
            with Session() as session:
                user = session.query(AccountModel).filter(
                    AccountModel.alternative_id == current_user.alternative_id).first()
                result = user.get_profile()
                return {"result": result}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def get_consultants():
        try:
            with Session() as session:
                users = session.query(AccountModel).filter(
                    AccountModel.role == UserTypeEnum.CONSULTANT).all()
                result = []

                for user in users:
                    data = user.get_profile()
                    data["id"] = user.id
                    result.append(data)
                return {"result": result}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def delete_account():
        try:
            with Session() as session:
                user = session.query(AccountModel).filter(
                    AccountModel.alternative_id == current_user.alternative_id).first()
                user.deleted = True
                user.date_of_account_removal = datetime.now()
                session.commit()
                return {"result": "Account deleted successfully"}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise

    @staticmethod
    def approve_consultant(consultant_id):
        try:
            with Session() as session:
                user = session.query(AccountModel).filter(
                    AccountModel.id == consultant_id).first()
                user.approved = True
                session.commit()

                return {"result": "Consultant approved successfully"}, 200
        except InvalidUserInput as err:
            return {"error": err.message}, 400
        except Exception:
            raise
