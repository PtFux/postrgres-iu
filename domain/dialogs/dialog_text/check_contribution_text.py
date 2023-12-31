from dataclasses import dataclass

from domain.dialogs.dialog_text.base_dialog_text import BaseDialogText
from domain.domain_model.filter import Filter


@dataclass
class CheckContributionText(BaseDialogText):
    NAME = "Проверка профзносов"

    ENTER_STUDENT_ID = "Пожалуйста, ввведите номер студенческого билета, профвзносы которого вы хотите проверить. \
                        Используйте /main чтобы выйти из режима проверки профвзносов в главное меню"
    NEED_REGISTRATION = f"Необходима регистрация. Пожалуйста, введите команду {Filter.COMMAND_START}"

    CONTRIBUTION_IS_PASSED = "Профзносы сданы"
    CONTRIBUTION_IS_NOT_PASSED = "Отказ от сдачи профвзносов"
    CONTRIBUTION_IS_NOT_KNOWN = "Нет информации"
    STUDENTSHIP = "Студент получает стипендию"
    CONTRIBUTION_IS_NOT_IN_DB = "Информация о студенте не внесена в систему"

    NOT_KNOWN = "Сообщение не распознано"
