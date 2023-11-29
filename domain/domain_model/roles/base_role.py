from dataclasses import dataclass

from common.user_role_code import UserRoleCode


@dataclass
class BaseRole:
    role_code = UserRoleCode.BASE

    can_check_contribution = False
    can_loading_data = False

    can_update_rating = False
    can_give_promo_code = False
    can_check_self_rating = False
    can_check_other_rating = False
    can_check_rating_stat = False
