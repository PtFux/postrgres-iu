from domain.domain_model.roles.base_role import BaseRole


class DutyRole(BaseRole):
    role_code = "duty"

    can_check_contribution = True

    can_check_self_rating = True
