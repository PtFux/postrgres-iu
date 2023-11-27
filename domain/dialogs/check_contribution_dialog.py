import logging
import re

from common.contribution_status import ContributionStatus
from domain.dialogs.dialog_base import DialogBase
from domain.dialogs.dialog_text.check_contribution_text import CheckContributionText
from domain.domain_model.filter import Filter
from domain.domain_model.message_domain import MessageDomain


class CheckContributionDialog(DialogBase):
    filter = Filter.CHECK_CONTRIBUTION

    def __init__(self, chat_id, storage, send_message):
        super().__init__(chat_id, storage, send_message)

    async def start(self, message: MessageDomain):
        logging.info(f"INFO: start check contribution dialog, text={message.text}")

        if await self._storage.check_registration_by_chat_id(message.chat_id):
            self.temp = self.wait_student_id_for_contribution
            await self._send_message(message.chat_id, CheckContributionText.ENTER_STUDENT_ID)
        else:
            await self._send_message(message.chat_id, CheckContributionText.NEED_REGISTRATION)
            return True

    async def wait_student_id_for_contribution(self, message: MessageDomain):
        if await self._check_right_student_id(message.text):
            await self._send_message(message.chat_id,
                                     await self._get_text_by_status_contribution_by_chat_id(message.text))
        else:
            await self._send_message(message.chat_id, CheckContributionText.NOT_KNOWN)
            await self._send_message(message.chat_id, CheckContributionText.ENTER_STUDENT_ID)

    async def _get_text_by_status_contribution_by_chat_id(self, chat_id: str):
        status = await self._storage.get_status_contribution_by_student_id_number(chat_id)
        match status:
            case ContributionStatus.NOT_KNOWN:
                return CheckContributionText.CONTRIBUTION_IS_NOT_KNOWN
            case ContributionStatus.PASSED:
                return CheckContributionText.CONTRIBUTION_IS_PASSED
            case ContributionStatus.STUDENTSHIP:
                return CheckContributionText.STUDENTSHIP
            case ContributionStatus.REFUSAL:
                return CheckContributionText.CONTRIBUTION_IS_NOT_PASSED
        return CheckContributionText.CONTRIBUTION_IS_NOT_IN_DB

    async def _check_right_student_id(self, student_id):
        return await self._storage.check_right_student_id(student_id)
