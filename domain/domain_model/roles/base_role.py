from dataclasses import dataclass


@dataclass
class BaseRole:
    role_code = "base"

    can_check_contribution = False
    can_loading_data = False

    can_update_rating = False
    can_give_promo_code = False
    can_check_self_rating = False
    can_check_other_rating = False
    can_check_rating_stat = False
