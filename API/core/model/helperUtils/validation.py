import re

from API.core.model.databaseModel import AccountModel


class Validation:
    @staticmethod
    def validate_email(incoming_email):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, incoming_email):
            return True
        from API.dbSession import Session
        with Session() as session:
            users = session.query(AccountModel).all()
            usernames = []
            for user in users:
                usernames.append(user.email)
            check = usernames.count(incoming_email)
            if check == 0:
                return True
            else:
                return False

    @staticmethod
    def validate_username(incoming_username):
        from API.dbSession import Session
        with Session() as session:
            users = session.query(AccountModel).all()
            usernames = []
            for user in users:
                usernames.append(user.username)
            check = usernames.count(incoming_username)
            if check == 0:
                return True
            else:
                return False

    @staticmethod
    def validate_update_username(incoming_username, user_id):
        from API.dbSession import Session
        with Session() as session:
            users = session.query(AccountModel).all()
            usernames = []
            for user in users:
                if user_id != user.alternative_id:
                    usernames.append(user.username)
            check = usernames.count(incoming_username)
            if check == 0:
                return True
            else:
                return False

    @staticmethod
    def validate_name(incoming_name):
        pass

    @staticmethod
    def validate_password(incoming_password):
        password_regex = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')
        if re.fullmatch(password_regex, incoming_password):
            return True
        else:
            return False

    @staticmethod
    def validate_region(incoming_region):
        if len(incoming_region) >= 2:
            return True
        else:
            return False
