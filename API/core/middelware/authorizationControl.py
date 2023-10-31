from flask_login import current_user

from API.core.model.enumTypes import UserTypeEnum


class ALC:
    @staticmethod
    def has_customer_privilege():
        if current_user.is_authenticated:
            return current_user.role is UserTypeEnum.USER
        else:
            return False

    @staticmethod
    def has_consultant_privilege():
        if current_user.is_authenticated:
            return current_user.role is UserTypeEnum.CONSULTANT
        else:
            return False

    @staticmethod
    def has_administrator_privilege():
        if current_user.is_authenticated:
            return current_user.role is UserTypeEnum.ADMIN
        else:
            return False

    @staticmethod
    def has_owner_privilege():
        if current_user.is_authenticated:
            return current_user.role is UserTypeEnum.OWNER
        else:
            return False
