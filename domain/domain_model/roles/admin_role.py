from domain.domain_model.roles.base_role import BaseRole


class AdminRole(BaseRole):
    role_code = "admin"

    can_check_contribution = True
    can_loading_data = True

    can_update_rating = True
    can_give_promo_code = False
    can_check_self_rating = True
    can_check_other_rating = True
    can_check_rating_stat = True
