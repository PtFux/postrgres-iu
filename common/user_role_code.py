from dataclasses import dataclass


@dataclass
class UserRoleCode:
    GOD = "god"
    ADMIN = "admin"
    DUTY = "duty"
    USER = "user"

    BASE = "base"

    UNKNOWN = "unknown"
