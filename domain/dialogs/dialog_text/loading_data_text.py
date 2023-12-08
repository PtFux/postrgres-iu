from dataclasses import dataclass

from domain.dialogs.dialog_text.base_dialog_text import BaseDialogText
from domain.domain_model.filter import Filter


@dataclass
class LoadingDataText(BaseDialogText):
    NAME = "Загрузка профвзносов"

    WRITE_CSV = "Введите, пожалуйста, таблицу в формате:\n<code>{table}</code>"

    WAIT_CSV = "Ожидается файл cvs формата в виде таблицы:\n<code>{table}</code>\nИспользуйте команду {main_cmd}, чтобы выйти"
    NEED_REGISTRATION = f"Необходима регистрация. Используйте команду {Filter.COMMAND_START}"
    EXCEPTION = "Не удалось загрузить данные."
    SUCCESSFUL = "Данные успешно загружены"

    CONFIRM_LOADING = "Подтвердите загрузку данных словом <code>{code_agree}</code>"
    AGREE_LOADING = "Да"
    TABLE_ST_CONT = "Информация о студентах:\n{student_table}\n\nИнформаця о профвзносах:\n{cont_table}\n\n"


