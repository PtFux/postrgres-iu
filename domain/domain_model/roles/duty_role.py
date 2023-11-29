from common.user_role_code import UserRoleCode
from domain.domain_model.roles.base_role import BaseRole


class DutyRole(BaseRole):
    role_code = UserRoleCode.DUTY

    can_check_contribution = True

    can_check_self_rating = True
