import logging

from domain.dialogs.dialog_base import DialogBase
from domain.dialogs.dialog_text.main_ratings_text import MainRatingsText
from domain.dialogs.dialog_text.user_role_update_text import UserRoleUpdateText
from domain.dialogs.kb.main_ratings_kb import MainRatingsKB
from domain.dialogs.kb.user_role_kb import UserRoleKB
from domain.domain_model.filter import Filter
from domain.domain_model.message_domain import MessageDomain
from domain.domain_model.promo_code_domain import PromoCodeDomain
from domain.domain_model.rating_domain import RatingDomain
from domain.domain_model.roles import AllRoles


class MainRatingsDialog(DialogBase):
    filter = Filter.MAIN_RATINGS
    right = "can_do_with_ratings"
    name = MainRatingsText.NAME

    def __init__(self, chat_id, storage, send_message):
        super().__init__(chat_id, storage, send_message)
        self._last_kb = None
        self._all_roles = AllRoles()
        self.rights = {
            "can_give_promo_code": {"name": "Выдать промокод", "func": self.get_new_promo_code_name,
                                    "first_m": MainRatingsText.ENTER_NEW_PROMO_CODE_NAME},
            "can_check_other_rating": {"name": "Посмотреть рейтинг", "func": self.check_other_rating,
                                       "first_m": MainRatingsText.ENTER_STUDENT_ID_FOR_RATINGS},
            "can_check_rating_stat": {"name": "Посмотреть топ", "func": self.check_rating_stat,
                                      "first_m": MainRatingsText.ENTER_NUMBER_FOR_TOP},
            "can_update_rating": {"name": "Изменить рейтинг", "func": self.get_student_id_for_update_rating,
                                  "first_m": MainRatingsText.ENTER_STUDENT_ID_FOR_RATINGS},
            "can_check_self_rating": {"name": "Посмотреть свой рейтинг", "func": self.check_self_rating,
                                      "first_m": MainRatingsText.ENTER_STUDENT_ID_FOR_RATINGS},
            "can_use_promo_code": {"name": "Промокод", "func": self.use_promo_code,
                                   "first_m": MainRatingsText.ENTER_PROMO_CODE}
        }

        self._promo_code: PromoCodeDomain = PromoCodeDomain()
        self._rating = RatingDomain()

    async def start(self, message: MessageDomain):
        logging.info(f"domain: start main ratings dialog, text={message.text}")

        role = await self._storage.get_user_role_by_chat_id(message.chat_id)
        markup_kb = await self._get_markup_kb_by_role(role)
        await self._send_message_with_kb(message.chat_id, MainRatingsText.CHOOSE_DO, markup_kb)
        self.temp = self.wait_right_for_ratings

    async def wait_right_for_ratings(self, message: MessageDomain):

        role_code = await self._storage.get_user_role_by_chat_id(message.chat_id)
        temp_right = self.rights.get(message.text)
        if not temp_right:
            markup_kb = await self._get_markup_kb_by_role(role_code)
            await self._send_message_with_kb(message.chat_id, MainRatingsText.NO_KNOWN, markup_kb)
            return

        enable_roles = self._all_roles.get_enable_role_code_by_atr_name(message.text)
        if role_code in enable_roles:
            self.temp = temp_right.get("func")
            await self._send_message(message.chat_id,
                                     temp_right.get("first_m"))
        else:
            markup_kb = await self._get_markup_kb_by_role(role_code)
            await self._send_message_with_kb(message.chat_id, MainRatingsText.PERMISSION_DENIED, markup_kb)

    async def _get_markup_kb_by_role(self, role_code: str):
        role = self._all_roles.get_role_by_role_code(role_code)
        if not role:
            return
        enable_rights = {
            right: self.rights.get(right) for right in self.rights.keys()
            if getattr(role, right, False)
        }
        kb = MainRatingsKB(enable_rights)
        return self._create_kb_builder(kb).as_markup()

    async def get_student_id_for_update_rating(self, message: MessageDomain):
        student_id = message.text.upper()
        if await self._storage.check_right_student_id(student_id):
            self._rating.student_id = student_id
            self.temp = self.get_amount_for_update_rating
            await self._send_message(message.chat_id, MainRatingsText.ENTER_ADD_AMOUNT_RATING)
        else:
            await self._send_message(
                message.chat_id,
                "\n\n".join((MainRatingsText.NO_KNOWN, MainRatingsText.ENTER_STUDENT_ID_FOR_RATINGS))
            )

    async def get_amount_for_update_rating(self, message: MessageDomain):
        if message.text.isdigit():
            try:
                self._rating.add_amount = int(message.text)
                not_exist_student = await self._add_amount_for_rating()
            except Exception as e:
                logging.exception(f"domain: dialog.ratings exception:{e}")
                await self._send_message(message.chat_id, MainRatingsText.EXCEPTION)
                return True
            if not_exist_student:
                await self._send_message(
                    message.chat_id,
                    MainRatingsText.OTHER_RATING_NO_IN_SYSTEM.format(student_id=self._rating.student_id)
                )
            else:
                await self._send_message(
                    message.chat_id,
                    MainRatingsText.SUCCESSFUL_ADDING_AMOUNT_FOR_RATINGS.format(
                        student_id=self._rating.student_id,
                        add_amount=self._rating.add_amount
                    )
                )
            await self._send_message(message.chat_id, MainRatingsText.ENTER_STUDENT_ID_FOR_RATINGS)
            self.temp = self.get_student_id_for_update_rating
        else:
            await self._send_message(
                message.chat_id,
                "\n\n".join((MainRatingsText.NO_KNOWN, MainRatingsText.ENTER_ADD_AMOUNT_RATING))
            )

    async def _add_amount_for_rating(self):
        return await self._storage.update_rating_by_student_id_on_amount(self._rating)

    async def get_new_promo_code_name(self, message: MessageDomain):
        """

        :param message: message.text is name for new promo code
        :return:
        """
        self._promo_code.name = message.text
        self.temp = self.get_new_promo_code_amount
        await self._send_message(message.chat_id, MainRatingsText.ENTER_PROMO_CODE_AMOUNT)

    async def get_new_promo_code_amount(self, message: MessageDomain):
        if message.text.isdigit():
            self._promo_code.amount = int(message.text)
            self.temp = self.get_new_promo_code_count
            await self._send_message(message.chat_id, MainRatingsText.ENTER_PROMO_CODE_COUNT)
        else:
            await self._send_message(message.chat_id, MainRatingsText.NO_KNOWN)
            await self._send_message(message.chat_id, MainRatingsText.ENTER_PROMO_CODE_AMOUNT)

    async def get_new_promo_code_count(self, message: MessageDomain):
        if message.text.isdigit():
            self._promo_code.count = int(message.text)
            self.temp = self.wait_access_for_promo_code
            await self._send_message(
                message.chat_id,
                MainRatingsText.ENTER_PROMO_CODE_ACCESS.format(promo_name=self._promo_code.name,
                                                               amount=self._promo_code.amount,
                                                               count=self._promo_code.count,
                                                               access=MainRatingsText.ENTER_AGREE,
                                                               not_access=MainRatingsText.ENTER_NOT_AGREE
                                                               ))
        else:
            await self._send_message(message.chat_id, MainRatingsText.NO_KNOWN)
            await self._send_message(message.chat_id, MainRatingsText.ENTER_PROMO_CODE_COUNT)

    async def wait_access_for_promo_code(self, message: MessageDomain):
        match message.text:
            case MainRatingsText.ENTER_AGREE:
                try:
                    await self.add_new_promo_code()
                except Exception:
                    await self._send_message(message.chat_id, MainRatingsText.EXCEPTION)
                    return True
                await self._send_message(message.chat_id, MainRatingsText.SUCCESSFUL_ADDING_NEW_PROMO_CODE)
                return True
            case MainRatingsText.ENTER_NOT_AGREE:
                await self._send_message(message.chat_id, MainRatingsText.ENTER_PROMO_CODE_AGAIN)
                await self._send_message(message.chat_id, MainRatingsText.ENTER_NEW_PROMO_CODE_NAME)
                self.temp = self.get_new_promo_code_name
            case _:
                await self._send_message(message.chat_id, MainRatingsText.NO_KNOWN)
                await self._send_message(
                    message.chat_id,
                    MainRatingsText.ENTER_PROMO_CODE_ACCESS.format(promo_name=self._promo_code.name,
                                                                   amount=self._promo_code.amount,
                                                                   count=self._promo_code.count,
                                                                   access=MainRatingsText.ENTER_AGREE,
                                                                   not_access=MainRatingsText.ENTER_NOT_AGREE
                                                                   ))

    async def add_new_promo_code(self):
        await self._storage.insert_new_promo_code(self._promo_code)

    async def check_self_rating(self, message: MessageDomain):
        rating = await self._storage.get_rating_by_user_chat_id(message.chat_id)
        if type(rating) is int:
            await self._send_message(message.chat_id, MainRatingsText.SELF_RATING.format(rating=rating))
            return True
        await self._send_message(message.chat_id, MainRatingsText.NO_IN_SYSTEM)
        return True

    async def check_other_rating(self, message: MessageDomain):
        student_id = message.text.upper()
        if await self._storage.check_right_student_id(student_id):
            rating = await self._storage.get_rating_by_student_id(student_id)
            if type(rating) is int:
                await self._send_message(message.chat_id, MainRatingsText.OTHER_RATING.format(student_id=student_id,
                                                                                              rating=rating))
                return
            await self._send_message(message.chat_id,
                                     MainRatingsText.OTHER_RATING_NO_IN_SYSTEM.format(student_id=student_id))
            return
        else:
            await self._send_message(message.chat_id, MainRatingsText.NO_RIGHT_STUDENT_ID_NUMBER)
            await self._send_message(message.chat_id, MainRatingsText.ENTER_STUDENT_ID_FOR_RATINGS)

    async def check_rating_stat(self, message: MessageDomain):
        print(message.text)

    async def use_promo_code(self, message: MessageDomain):
        pass
