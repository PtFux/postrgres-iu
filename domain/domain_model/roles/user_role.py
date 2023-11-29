from common.user_role_code import UserRoleCode
from domain.domain_model.roles.base_role import BaseRole


class UserRole(BaseRole):
    role_code = UserRoleCode.USER

    can_check_contribution = True
