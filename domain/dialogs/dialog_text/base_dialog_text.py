from dataclasses import dataclass

from domain.domain_model.filter import Filter


@dataclass
class BaseDialogText:
    PERMISSION_DENIED = f"Нет доступа для вашей роли. Пожалуйста, используйте команду {Filter.MAIN_MENU}"
    NEED_REGISTRATION = (f"Для работы в системе необходимо зарегистрироватьс. \
    Пожалуста, используте команду {Filter.COMMAND_START}")
    NO_KNOWN = "Сообщение не распознано"
