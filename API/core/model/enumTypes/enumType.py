from enum import Enum


class AccessLevelAction(Enum):
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"


class AccountStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REMOVED = "removed"


class LoginStatus(Enum):
    LOGGED_IN = "online"
    LOGGED_OUT = "offline"


class UserTypeEnum(Enum):
    USER = "User"
    ADMIN = "Admin"
    CONSULTANT = "Consultant"
    SUPER_ADMIN = "Super Admin"
    OWNER = "Owner"


class QuestionCategory(Enum):
    CLIENT_QUIZ = "Client Quiz"
    CONSULTANT_QUIZ = "Consultant Quiz"


class MeetingType(Enum):
    VIDEO_CALL = "Video Call"
    TEXT_CHAT = "Text Chat"
    PHONE_CALL = "Phone Call"
