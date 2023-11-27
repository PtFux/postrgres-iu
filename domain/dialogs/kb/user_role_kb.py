from domain.dialogs.kb.base_kb import Button, BaseKB


class UserRole:
    ADMIN = "admin_role"
    MODERATOR = "moderator_role"
    DUTY = "duty_role"

    @staticmethod
    def values():
        return [
            UserRole.ADMIN,
            UserRole.MODERATOR,
            UserRole.DUTY
        ]


class UserRoleKB(BaseKB):
    buttons = {
        UserRole.ADMIN:
        Button("Я администратор",
               UserRole.ADMIN),
        UserRole.MODERATOR:
        Button("Я модератор",
               UserRole.MODERATOR),
        UserRole.DUTY:
        Button("Я дежурный",
               UserRole.DUTY)
    }
