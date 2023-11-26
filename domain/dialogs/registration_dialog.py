from domain.dialogs.dialog_base import DialogBase
from domain.domain_model.filter import Filter
from domain.domain_model.message_domain import MessageDomain
from domain.dialogs.kb.start_registration_student_id_kb import StartRegistrationStudentIdKB, StatusStudent
from domain.dialogs.registration_text import RegistrationText


class RegistrationDialog(DialogBase):
    filter = Filter.COMMAND_START

    def __init__(self, chat_id, storage, send_message):
        super().__init__(chat_id, storage)
        self._last_kb = None
        self.__send_message = send_message

    async def start(self, message: MessageDomain):
        """
        Для работы с системой надо зарегистрироваться
        Кидаем табличку
        Введу номер студенченского билета | Не студент МГТУ
        РЕГИСТРАЦИЯ
        :param message:
        :return:
        """

        self._last_kb = StartRegistrationStudentIdKB()
        await self._send_message(message.chat_id, RegistrationText.HELLO)
        await self._send_message(message.chat_id, RegistrationText.NEED_REGISTRATION)
        # await self._send_kb(self._last_kb)
        self.temp = self.get_status_student_or_no_student

    async def get_status_student_or_no_student(self, message: MessageDomain):
        if message.text == self._last_kb.buttons.get(StatusStudent.STUDENT).reply_text or \
           message.reply_text == self._last_kb.buttons.get(StatusStudent.STUDENT).reply_text:
            "Отправляем сообщение, что нужно отправить студенческий ID"
            self.temp = self.wait_student_id
            await self._send_message(message.chat_id, RegistrationText.NEED_STUDENT_ID)
        elif message.text == self._last_kb.buttons.get(StatusStudent.NO_STUDENT).reply_text or \
             message.reply_text == self._last_kb.buttons.get(StatusStudent.NO_STUDENT).reply_text:
            "Отправляем, что регистрация для не студентов, к сожалению невозможна"
            await self._send_message(message.chat_id, RegistrationText.NO_STUDENT)
        else:
            "Отправляем что сообщение не распознано. Отправляем таблицу"
            await self._send_message(message.chat_id, RegistrationText.NO_KNOWN)
            await self._send_kb(self._last_kb)

    async def wait_student_id(self, message: MessageDomain):
        pass

    async def _send_kb(self, kb):
        pass

    async def _send_message(self, chat_id: str, text: str):
        await self.__send_message(
            chat_id,
            text
        )


