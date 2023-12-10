import logging
import re
from typing import Any

from common.contribution_status import ContributionStatus
from common.user_role_code import UserRoleCode
from domain.domain_model.contribution import Contribution
from domain.domain_model.promo_code_domain import PromoCodeDomain
from domain.domain_model.rating_domain import RatingDomain
from domain.domain_model.student_domain import StudentDomain
from service.repositories.postgres_repository import PostgresRepository
from service.settings.postgres_settings import PostgresSettings
from service.settings.default_postgres_settings import DEFAULT_POSTGRES_SETTINGS


class Storage:
    def __init__(self, connection: PostgresSettings = None):
        if not connection:
            connection = DEFAULT_POSTGRES_SETTINGS
        self._repository = PostgresRepository(connection)

    async def start(self):
        await self._repository.initialize()

    async def add_user(self, chat_id: str, student_id: str, tg_name: str = "", role_code: str = UserRoleCode.USER):
        logging.info(f"Storage: Added new default user with chat_id = {chat_id}")

        await self._repository.insert_user_with_student_id_number_and_role_code_name(
            student_id_number=student_id,
            role_code_name=role_code,
            telegram=chat_id,
            tg_name=tg_name
        )
        return True

    async def check_registration_by_chat_id(self, chat_id: str):
        role = await self._repository.select_user_role_by_chat_id(chat_id)
        logging.info(f"Storage: Check role={role} by chat_id={chat_id}")
        return role is not None

    async def get_status_contribution_by_student_id_number(self, student_id_number: str) -> ContributionStatus:
        status_contribution = await self._repository.get_status_contribution_by_student_id_number(student_id_number)

        logging.info(f"Storage: Check status contribution={status_contribution} by student={student_id_number}")
        if status_contribution:
            return ContributionStatus(status_contribution)
        else:
            return ContributionStatus.NOT_KNOWN

    async def get_admin_chat_id(self):
        return "748216079"

    async def select_top_rating(self, size: int):
        return await self._repository.select_top_rating(size)

    async def get_user_role_by_chat_id(self, chat_id: str, default=UserRoleCode.UNKNOWN):
        role = await self._repository.select_user_role_by_chat_id(chat_id)
        logging.info(f"Storage: Check role={role} by chat_id={chat_id}")
        return role if role else default

    async def get_rating_by_user_chat_id(self, chat_id: str) -> int | None:
        return await self._repository.get_rating_by_user_chat_id(chat_id)

    async def get_rating_by_student_id(self, student_id_number: str) -> int | None:
        rating = await self._repository.get_rating_by_student_id(student_id_number)
        logging.info(f"Storage: Got rating={rating} of student_id {student_id_number}")
        return rating

    async def update_rating_by_student_id_on_amount(self, rating: RatingDomain):
        logging.info(f"Storage: get update rating student={rating.student_id} for amount={rating.add_amount}")
        return await self._repository.update_rating_by_student_id_number(
            student_id_number=rating.student_id,
            add_amount=rating.add_amount
        )

    async def check_right_student_id(self, student_id_number):
        return re.fullmatch(r'\d\d\w\d\d\d\d', student_id_number)

    async def insert_students(self, students: list[dict | Any]):
        not_exist_student = []
        for student in students:
            if not await self._repository.select_student_id_by_student_id_number(student.get("student_id_number")):
                not_exist_student.append(student)
        await self._repository.insert_many_student(not_exist_student)
        logging.info(f"Storage: Added next students={not_exist_student}")
        return not_exist_student

    async def insert_contributions(self, contributions: list[Contribution]):
        not_exit_contributions = []
        not_right_contributions = []
        for cont in contributions:
            status = await self._repository.select_status_cont_by_season_student_id_number(cont.student_id_number,
                                                                                           season=int(cont.season.value),
                                                                                           year=cont.year)
            if status is None:
                not_exit_contributions.append(cont)
            elif ContributionStatus(status) != cont.status:
                not_right_contributions.append(cont)

        await self._repository.insert_many_contributions(not_exit_contributions)
        logging.info(f"Storage: Added next contributions={not_exit_contributions}")

        for cont in not_right_contributions:
            await self._repository.update_cont_by_student_id_number_season_and_year(cont)
        logging.info(f"Storage: Updated next contributions={not_right_contributions}")

    async def insert_default_ratings_for_many_students(self, students: list[dict | StudentDomain], amount: int = 0):
        ratings = []
        for student in students:
            ratings.append(
                RatingDomain(
                    student_id=await self._repository.select_student_id_by_student_id_number(student.student_id_number),
                    amount=amount
                )
            )
        if ratings:
            await self._repository.insert_many_ratings(ratings)

    async def insert_new_promo_code(self, promo_code: PromoCodeDomain):
        await self._repository.insert_one_promo_code(
            code=promo_code.name, amount=promo_code.amount, count=promo_code.count
        )

    async def get_amount_by_promo_code(self, code: str) -> int | None:
        return await self._repository.get_amount_by_promo_code(code)

    async def check_using_promo_code(self, promo_name: str, telegram: str) -> Any | None:
        return await self._repository.get_using_promo_code(promo_name, telegram)

    async def update_rating_by_telegram_on_amount(self, telegram: str, add_amount: int):
        await self._repository.update_rating_by_telegram(telegram, add_amount)

    async def add_using_promo_code(self, code: str, telegram: str):
        await self._repository.insert_one_using_promo_code(code, telegram)

    async def pop_promo_code_and_get_count(self, code: str) -> int:
        await self._repository.update_count_of_promo_code(code, add_count=-1)
        return await self._repository.get_count_promo_code(code)

    async def delete_info_about_promo_code(self, code: str):
        await self._repository.delete_one_promo_code(code)
        await self._repository.delete_all_using_promo_code(code)

