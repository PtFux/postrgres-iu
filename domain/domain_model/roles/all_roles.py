from admin_role import AdminRole
from domain.domain_model.roles.base_role import BaseRole
from domain.domain_model.roles.duty_role import DutyRole
from domain.domain_model.roles.god_role import GodRole
from domain.domain_model.roles.user_role import UserRole


class AllRoles:
    roles = [UserRole, DutyRole, AdminRole, GodRole]

    def __init__(self):
        self.roles_by_code = {role.role_code: role for role in self.roles}

    def get_role_codes(self):
        return self.roles_by_code.keys()

    @staticmethod
    def get_all_rights():
        return [
            atr for atr in dir(BaseRole) if atr.startswith("can")
        ]

    def get_enable_role_by_atr_name(self, atr_name: str):
        return [
            role for role in self.roles if getattr(role, atr_name)
        ]


if __name__ == "__main__":
    rb = RoleRights()
    print("kjdskjd", rb.roles_by_code)
    print(rb.get_role_codes())
    print(rb.get_all_rights())
    print(rb.get_enable_role_by_atr_name("can_give_promo_code"))
