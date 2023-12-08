from dataclasses import dataclass

from domain.dialogs.dialog_text.base_dialog_text import BaseDialogText


@dataclass
class RegistrationText(BaseDialogText):
    NAME = "Регистрация"

    HELLO = "Вас приветствует бот для проверки профвзносов и баллов рейтинга активиста профсоюза ИУ"

    REGISTRATION = "РЕГИСТРАЦИЯ"
    NEED_STUDENT_ID = "Пожалуйста, отправьте номер своего студенческого билета"
    NO_STUDENT = "Регистрация для не студентов ИУ МГТУ, к сожалению, невозможна"

    # wait student id
    AGAIN_REGISTRATION = "Вы уже регистрировалсь ранее."
    SUCCESSFUL_REGISTRATION = "Успешная регистрация!"
    NOT_SUCCESSFUL_REGISTRATION = "Недачная попытка."

    MESSAGE_FOR_ADMIN = "Пользователь @{username} со студенческим биелтом {student_id} \
    успешно зарегистрировался в системе"
