from domain.domain_model.roles.base_role import BaseRole


class UserRole(BaseRole):
    role_code = "user"
    can_check_contribution = True
