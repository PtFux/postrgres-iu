from dataclasses import dataclass


@dataclass
class RegistrationText:
    HELLO = "Вас приветствует бот для проверки профвзносов и баллов рейтинга активиста профсоюза ИУ"
    NEED_REGISTRATION = "Для работы в системе необходимо зарегистрироваться"
    REGISTRATION = "РЕГИСТРАЦИЯ"
    NEED_STUDENT_ID = "Пожалуйста, отправьте номер своего студенческого билета"
    NO_STUDENT = "Регистрация для не студентов ИУ МГТУ, к сожалению, невозможна"
    NO_KNOWN = "Сообщение не распознано, пожалуйста, используйте кнопки"

    # wait student id
    AGAIN_REGISTRATION = "Вы уже регистрировалсь ранее."
    SUCCESSFUL_REGISTRATION = "Успешная регистрация!"
    NOT_SUCCESSFUL_REGISTRATION = "Недачная попытка. Напишит администратору @PtFux"