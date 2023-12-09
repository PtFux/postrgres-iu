from dataclasses import dataclass

from domain.dialogs.dialog_text.base_dialog_text import BaseDialogText
from domain.domain_model.filter import Filter


@dataclass
class MainRatingsText(BaseDialogText):
    NAME = "Рейтинг"

    CHOOSE_DO = "Балльно-рейтинговая система Профсоюза ИУ. Пожалуйста, выберите действие"
    ACCESS_MOVE_TO = "Подтвердить переход в '{button_name}'"

    ENTER_NEW_PROMO_CODE_NAME = "Введите название нового промокода"
    ENTER_NUMBER_FOR_TOP = "Напишите размер топа. Необходимо отправить число"
    ENTER_STUDENT_ID_FOR_RATINGS = "Введите номер студенческого билета. Используйте большие русские буквы."
    ENTER_PROMO_CODE = "Введите свой промокод"

    ENTER_PROMO_CODE_AMOUNT = "Введите значение нового промокода (число)"
    ENTER_PROMO_CODE_COUNT = "Введите количество использования промокода (число)"
    ENTER_PROMO_CODE_ACCESS = "Подтвердите добавление нового промокода <code>{promo_name}</code> \
    со значением <b>{amount}</b> и количествои использований, равным <b>{count}</b>. \
    Используйте слово <code>{access}</code> для подтверждения либо слово <code>{not_access}</code> для изменения промокода."

    ENTER_AGREE = "ДА"
    ENTER_NOT_AGREE = "НЕТ"

    SUCCESSFUL_ADDING_NEW_PROMO_CODE = "Новый промокод успешно добавлен!"
    EXCEPTION = "Неудачная попытка. Обратитесь к администратору"

    ENTER_PROMO_CODE_AGAIN = "Пожалуйста, заполните введите все данные снова."

    SELF_RATING = "Ваш рейтинг равен <b>{rating}</b>. Поздравляем, это отличный результат!"
    NO_IN_SYSTEM = "Вас еще нет в нашей системе( Обратитесь за помощью к профоргу группы!"
    OTHER_RATING = "Рейтинг студента со студенческим {student_id} равен {rating}"
    OTHER_RATING_NO_IN_SYSTEM = "Студента со студенческим {student_id} все еще нет в нашей системе"
    NO_RIGHT_STUDENT_ID_NUMBER = "Неверный номер студенческого. Попробуйте еще раз."

    ENTER_ADD_AMOUNT_RATING = "Введите число, на значение которого вы хотите изменить рейтинг"
    SUCCESSFUL_ADDING_AMOUNT_FOR_RATINGS = "Рейтинг студента {student_id} успешно изменен на значение {add_amount}"
