from typing import Any


from sqlalchemy import select, update, UUID, delete

from domain.domain_model.rating_domain import RatingDomain
from service.repositories.base.base_repository import BaseRepository
from service.settings.postgres_settings import PostgresSettings

from .entities import *
from .entities.promo_code_entity import PromoCodeEntity
from .entities.using_promo_code_entity import UsingPromoCodeEntity


class PostgresRepository(BaseRepository):
    def __init__(self, connection_setting: PostgresSettings, echo_logs=False):
        super().__init__(connection_setting, echo_logs)

    async def insert_one_contribution(self, amount: int, student_id_number: str, season: int, year: int, status: int):
        student_id = await self.select_student_id_by_student_id_number(student_id_number)

        entity = ContributionEntity(
            amount=amount,
            student_id=student_id,
            season=season,
            year=year,
            status=status
        )
        return await self._insert_one(entity)

    async def insert_many_contributions(self, many_contribution: list[dict | Any]):
        entities = []
        for contribution in many_contribution:
            student_id = await self.select_student_id_by_student_id_number(contribution.get("student_id_number"))
            entities.append(ContributionEntity(
                amount=contribution.get("amount"),
                student_id=student_id,
                season=int(contribution.get("season")),
                year=contribution.get("year"),
                status=int(contribution.get("status"))
            ))
        return await self._insert_many(entities)

    async def insert_student(self, name: str, surname: str, student_id_number: str):
        entity = StudentEntity(
            name=name,
            surname=surname,
            student_id_number=student_id_number
        )
        return await self._insert_one(entity)

    async def insert_many_student(self, students: list[dict | Any]):
        entities = [StudentEntity(
            name=student.get("name"),
            surname=student.get("surname"),
            student_id_number=student.get("student_id_number")
        ) for student in students]
        return await self._insert_many(entities)

    async def insert_one_promo_code(self, code: str, amount: int, count: int):
        entity = PromoCodeEntity(
            code=code,
            amount=amount,
            count=count
        )
        return await self._insert_one(entity)

    async def insert_one_using_promo_code(self, code: str, telegram: str):
        promo_code_id = await self._get_promo_code_id_by_code(code)
        student_id = await self._get_student_id_by_telegram(telegram)

        entity = UsingPromoCodeEntity(
            promo_code_id=promo_code_id,
            student_id=student_id
        )
        return await self._insert_one(entity)

    async def select_user_role_by_chat_id(self, tg_id: str):
        stmt = select(UserEntity.role_code).where(UserEntity.telegram == tg_id)
        return await self._select_one(stmt)

    async def get_status_contribution_by_student_id_number(self, student_id_number: str):
        stmt = select(StudentEntity.student_id).where(StudentEntity.student_id_number == student_id_number)
        student_id: UUID = await self._select_one(stmt)
        stmt = select(ContributionEntity.status).where(ContributionEntity.student_id == student_id)
        return await self._select_one(stmt)

    async def get_rating_by_user_chat_id(self, telegram: str):
        stmt = select(UserEntity.student_id).where(UserEntity.telegram == telegram)
        student_id: UUID = await self._select_one(stmt)
        stmt = select(RatingEntity.amount).where(RatingEntity.student_id == student_id)
        return await self._select_one(stmt)

    async def get_rating_by_student_id(self, student_id_number: str):
        student_id: UUID = await self.select_student_id_by_student_id_number(student_id_number)
        stmt = select(RatingEntity.amount).where(RatingEntity.student_id == student_id)
        return await self._select_one(stmt)

    async def get_amount_by_promo_code(self, code: str) -> int | None:
        stmt = select(PromoCodeEntity.amount).where(PromoCodeEntity.code == code)
        return await self._select_one(stmt)

    async def get_using_promo_code(self, promo_code_name: str, telegram: str):
        stmt = select(UsingPromoCodeEntity).join(PromoCodeEntity).join(StudentEntity).join(UserEntity).where(
            PromoCodeEntity.code == promo_code_name,
            UserEntity.telegram == telegram
        )
        return await self._select_one(stmt)

    async def get_count_promo_code(self, code: str):
        stmt = select(PromoCodeEntity.count).where(PromoCodeEntity.code == code)
        return await self._select_one(stmt)

    async def _get_promo_code_id_by_code(self, code: str) -> UUID:
        stmt = select(PromoCodeEntity.promo_code_id).where(PromoCodeEntity.code == code)
        return await self._select_one(stmt)

    async def _get_user_id_by_telegram(self, telegram: str) -> UUID:
        stmt = select(UserEntity.user_id).where(UserEntity.telegram == telegram)
        return await self._select_one(stmt)

    async def select_student_id_by_student_id_number(self, student_id_number: str):
        stmt = select(StudentEntity.student_id).where(StudentEntity.student_id_number == student_id_number)
        return await self._select_one(stmt)

    async def select_top_rating(self, size: int):
        stmt = select(StudentEntity.surname, StudentEntity.student_id_number, RatingEntity.amount).\
            join(RatingEntity).order_by(-RatingEntity.amount).limit(size)
        return await self._select_many(stmt)

    async def select_status_cont_by_season_student_id_number(self, student_id_number: str, season: int, year: int):
        stmt = select(StudentEntity.student_id).where(StudentEntity.student_id_number == student_id_number)
        student_id = await self._select_one(stmt)
        stmt = select(ContributionEntity.status).where(
            (ContributionEntity.student_id == student_id) and
            (ContributionEntity.season == season) and
            (ContributionEntity.year == year)
        )
        return await self._select_one(stmt)

    async def update_cont_by_student_id_number_season_and_year(self, cont: dict | Any):
        stmt = select(StudentEntity.student_id).where(
            StudentEntity.student_id_number == str(cont.get("student_id_number")))
        student_id = await self._select_one(stmt)
        stmt = update(ContributionEntity).values(
            amount=cont.get("amount"),
            status=int(cont.get("status"))
        ).where(
            (ContributionEntity.student_id == student_id) and
            (ContributionEntity.season == int(cont.get("season"))) and
            (ContributionEntity.year == cont.get("year"))
        )
        return await self._query_without_result(stmt)

    async def update_rating_by_student_id_number(self, student_id_number: str, add_amount: int = 0,
                                                 amount: int = -1, last_amount: int = -1):
        student_id: UUID = await self.select_student_id_by_student_id_number(student_id_number)
        if not student_id:
            return True

        return await self._update_rating_by_student_id(student_id, add_amount, amount, last_amount)

    async def _update_rating_by_student_id(self, student_id: UUID, add_amount: int = 0,
                                           amount: int = -1, last_amount: int = -1):

        stmt = select(RatingEntity).where(RatingEntity.student_id == student_id)
        entity = await self._select_one(stmt)

        if entity:
            amount = entity.amount + add_amount if amount == -1 else amount + add_amount
            stmt = update(
                RatingEntity
            ).values(
                amount=amount,
                last_amount=entity.amount if last_amount == -1 else last_amount
            ).where(
                (RatingEntity.student_id == student_id)
            )
            return await self._query_without_result(stmt)

        entity = RatingEntity(
            student_id=student_id,
            amount=add_amount if amount == -1 else amount,
            last_amount=last_amount
        )
        return await self._insert_one(entity)

    async def update_rating_by_telegram(self, telegram: str, amount: int):
        student_id: UUID = await self._get_student_id_by_telegram(telegram)
        if not student_id:
            return True

        return await self._update_rating_by_student_id(student_id, add_amount=amount)

    async def update_count_of_promo_code(self, code: str, add_count: int):
        query = update(PromoCodeEntity).values(
            count=PromoCodeEntity.count + add_count
        ).where(PromoCodeEntity.code == code)
        return await self._query_without_result(query)

    async def _get_student_id_by_telegram(self, telegram: str) -> UUID:
        stmt = select(UserEntity.student_id).where(UserEntity.telegram == telegram)
        return await self._select_one(stmt)

    async def insert_many_ratings(self, ratings: list[RatingDomain]):
        entities = []
        for rating in ratings:
            entities.append(
                RatingEntity(
                    student_id=rating.student_id,
                    amount=rating.amount,
                )
            )
        return await self._insert_many(entities)

    async def insert_user_with_student_id_number_and_role_code_name(self, student_id_number: str, role_code_name: str,
                                                                    telegram: str, tg_name: str = ""):
        student_id = await self.select_student_id_by_student_id_number(student_id_number)

        entity = UserEntity(
            student_id=student_id,
            role_code=role_code_name,
            telegram=telegram,
            tg_name=tg_name
        )

        return await self._insert_one(entity)

    async def get_student_id_number_by_telegram(self, telegram: str):
        stmt = select(UserEntity.student_id).where(UserEntity.telegram == telegram)
        student_id = str(await self._select_one(stmt))
        stmt = select(StudentEntity.student_id_number).where(StudentEntity.student_id == student_id)
        return await self._select_one(stmt)

    async def delete_one_promo_code(self, code: str):
        query = delete(PromoCodeEntity).where(PromoCodeEntity.code == code)
        return await self._query_without_result(query)

    async def delete_all_using_promo_code(self, code):
        code_id = await self._get_promo_code_id_by_code(code)
        query = delete(UsingPromoCodeEntity).where(UsingPromoCodeEntity.promo_code_id == code_id)
        return await self._query_without_result(query)
