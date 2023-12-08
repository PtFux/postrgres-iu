from dataclasses import dataclass

from domain.dialogs.dialog_text.base_dialog_text import BaseDialogText
from domain.domain_model.filter import Filter


@dataclass
class MainRatingsText(BaseDialogText):
    NAME = "Рейтинг"

    CHOOSE_DO = "Балльно-рейтинговая система Профсоюза ИУ. Пожалуйста, выберите действие"
    ACCESS_MOVE_TO = "Подтвердить переход в '{button_name}'"

    ENTER_NEW_PROMO_CODE_NAME = "Введите название нового промокода"
    ENTER_NUMBER_FOR_TOP = "Напишите размер топа. Необходимо отправить число"
    ENTER_STUDENT_ID_FOR_RATINGS = "Введите номер студенческого билета"
    ENTER_PROMO_CODE = "Введите свой промокод"
