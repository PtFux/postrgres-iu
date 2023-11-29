from dataclasses import dataclass

from domain.dialogs.dialog_text.base_dialog_text import BaseDialogText
from domain.domain_model.filter import Filter


@dataclass
class MainRatingsText(BaseDialogText):
    CHOOSE_DO = "Балльно-рейтинговая система Профсоюза ИУ. Пожалуйста, выберите действие"
    ACCESS_MOVE_TO = "Подтвердить переход в '{button_name}'"
