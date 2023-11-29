from domain.domain_model.roles.base_role import BaseRole
from domain.domain_model.roles.duty_role import DutyRole
from domain.domain_model.roles.god_role import GodRole
from domain.domain_model.roles.user_role import UserRole
from domain.domain_model.roles.admin_role import AdminRole


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

    def get_enable_role_code_by_atr_name(self, atr_name: str):
        return [
            role.role_code for role in self.roles if getattr(role, atr_name)
        ]

    def get_role_by_role_code(self, role_code: str):
        return self.roles_by_code.get(role_code)

    @staticmethod
    def get_enable_rights_by_role_and_rights(role: BaseRole, rights: list[str]) -> list[str]:
        return [
            right for right in rights
            if getattr(role, right, False)
        ]


if __name__ == "__main__":
    rb = AllRoles()
    print("kjdskjd", rb.roles_by_code)
    print(rb.get_role_codes())
    print(rb.get_all_rights())
    print(rb.get_enable_role_code_by_atr_name("can_give_promo_code"))
