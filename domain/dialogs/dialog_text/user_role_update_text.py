from dataclasses import dataclass


@dataclass
class UserRoleUpdateText:
    CHOOSE_ROLE = "Выберите роль, которую хотите запросить"
    NEED_REGISTRATION = "Необходима регистрация. Пожалуста, используте команду /start"
    QUERY_IS_SENDED = "Заявка на изменение роли отправлена администратору, пожалуйста, ожидайте"

    QUERY_FOR_ROLE = "Следущий пользователь @{0} запрашивает роль {1}"
    NOT_KNOWN = "Роль не распознана, пожалуйста, используйте кнопки"
