from dataclasses import dataclass

from common.user_role_code import UserRoleCode


@dataclass
class BaseRole:
    role_code = UserRoleCode.BASE

    can_update_self_user_role = True
    can_check_contribution = False
    can_loading_data = False
    can_do_with_ratings = True
    can_do_with_main_menu = True
    can_registration = False

    can_update_rating = False
    can_give_promo_code = False
    can_check_self_rating = False
    can_check_other_rating = False
    can_check_rating_stat = False
    can_use_promo_code = True
