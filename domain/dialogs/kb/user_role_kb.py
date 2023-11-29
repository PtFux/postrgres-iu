from domain.dialogs.kb.base_kb import Button, BaseKB
from domain.domain_model.roles import *


class UserRoleKB(BaseKB):
    buttons = {
        AdminRole.role_code:
        Button("Я администратор",
               AdminRole.role_code),
        DutyRole.role_code:
        Button("Я дежурный",
               DutyRole.role_code)
    }
