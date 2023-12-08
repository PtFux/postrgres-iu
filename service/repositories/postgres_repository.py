from typing import Any


from sqlalchemy import select, update

from domain.domain_model.rating_domain import RatingDomain
from service.repositories.base.base_repository import BaseRepository
from service.settings.postgres_settings import PostgresSettings

from .entities import *


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

    async def select_user_role_by_chat_id(self, tg_id: str):
        stmt = select(UserEntity.role_code).where(UserEntity.telegram == tg_id)
        return await self._select_one(stmt)

    async def get_status_contribution_by_student_id_number(self, student_id_number: str):
        print("GET ", student_id_number)
        stmt = select(StudentEntity.student_id).where(StudentEntity.student_id_number == student_id_number)
        student_id = await self._select_one(stmt)
        print("GET student_id", student_id, type(student_id))
        stmt = select(ContributionEntity.status).where(ContributionEntity.student_id == student_id)
        print("STMT", stmt)
        return await self._select_one(stmt)

    async def select_student_id_by_student_id_number(self, student_id_number: str):
        stmt = select(StudentEntity.student_id).where(StudentEntity.student_id_number == student_id_number)
        return await self._select_one(stmt)

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
        stmt = select(StudentEntity.student_id).where(StudentEntity.student_id_number == cont.get("student_id_number"))
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
        student_id = self.select_student_id_by_student_id_number(student_id_number)

        stmt = select(RatingEntity).where(RatingEntity.student_id == student_id)
        entity = await self._select_one(stmt)

        if entity:
            amount = entity.amount + add_amount if amount == -1 else amount
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
