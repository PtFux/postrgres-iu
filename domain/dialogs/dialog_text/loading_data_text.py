from dataclasses import dataclass

from domain.domain_model.filter import Filter


@dataclass
class LoadingDataText:
    WRITE_CSV = "Введите, пожалуйста, таблицу в формате:\n<code>{table}</code>"
    PERMISSION_DENIED = f"Нет доступа для вашей роли. Пожалуйста, используйте команду {Filter.MAIN_MENU}"
    WAIT_CSV = "Ожидается файл cvs формата в виде таблицы:\n<code>{table}</code>\nИспользуйте команду {main_cmd}, чтобы выйти"
    NEED_REGISTRATION = f"Необходима регистрация. Используйте команду {Filter.COMMAND_START}"
    EXCEPTION = "Не удалось загрузить данные."
    SUCCESSFUL = "Данные успешно загружены"


