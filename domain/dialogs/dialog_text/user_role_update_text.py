from dataclasses import dataclass

from domain.dialogs.dialog_text.base_dialog_text import BaseDialogText
from domain.domain_model.filter import Filter


@dataclass
class UserRoleUpdateText(BaseDialogText):
    CHOOSE_ROLE = "Выберите роль, которую хотите запросить"

    QUERY_IS_SENDED = "Заявка на изменение роли отправлена администратору, пожалуйста, ожидайте"

    QUERY_FOR_ROLE = "Пользователь @{username} запрашивает роль <b>{role}</b>. \
                      \nВыдать права командой <code>{give_role_cmd} {chat_id} {role} </code>"
    NOT_KNOWN = "Роль не распознана, пожалуйста, используйте кнопки"
