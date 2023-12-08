from dataclasses import dataclass

from domain.dialogs.dialog_text.base_dialog_text import BaseDialogText
from domain.domain_model.filter import Filter


@dataclass
class MainMenuText(BaseDialogText):
    START = "Добро пожаловать систему Профсоюза ИУ!"
    CHOOSE_DO = "Пожалуйста, выберите дейстиве"
