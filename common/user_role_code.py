from dataclasses import dataclass


@dataclass
class UserRoleCode:
    GOD = "god"
    ADMIN = "admin"
    DUTY = "duty"
    MODERATOR = "moderator"
    USER = "user"
