from sqlalchemy import select, update

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

    async def insert_student(self, name: str, surname: str, student_id_number: str):
        entity = StudentEntity(
            name=name,
            surname=surname,
            student_id_number=student_id_number
        )
        return await self._insert_one(entity)

    async def inset_many_student(self, students: list[dict]):
        entities = [StudentEntity(
            name=student.get("name"),
            surname=student.get("surname"),
            student_id_number=student.get("student_id_number")
        ) for student in students]
        return await self._insert_many(entities)

    async def select_student_id_by_student_id_number(self, student_id_number: str):
        stmt = select(StudentEntity.student_id).where(StudentEntity.student_id_number == student_id_number)
        return await self._select_one(stmt)

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

    async def insert_right(self, name: str, description: str):
        entity = RightEntity(
            name=name,
            description=description
        )
        return await self._insert_one(entity)

    async def insert_role(self, code_name: str, description: str):
        entity = RoleEntity(
            code_name=code_name,
            description=description
        )
        return await self._insert_one(entity)

    async def insert_rule_with_role_code_name_and_right_name(self, role_code_name: str, right_name: str):
        stmt = select(RoleEntity.role_id).where(RoleEntity.code_name == role_code_name)
        role_id = await self._select_one(stmt)
        stmt = select(RightEntity.right_id).where(RightEntity.name == right_name)
        right_id = await self._select_one(stmt)

        entity = RuleEntity(
            role_id=role_id,
            right_id=right_id
        )
        return await self._insert_one(entity)

    async def insert_user_with_student_id_number_and_role_code_name(self, student_id_number: str, role_code_name: str,
                                                                    telegram: str, telephone: str = None):
        student_id = await self.select_student_id_by_student_id_number(student_id_number)
        role_id = await self._select_one(select(RoleEntity.role_id).where(RoleEntity.code_name == role_code_name))
        if telephone:
            entity = UserEntity(
                student_id=student_id,
                role_id=role_id,
                telegram=telegram,
                telephone=telephone
            )
        else:
            entity = UserEntity(
                student_id=student_id,
                role_id=role_id,
                telegram=telegram,
            )
        return await self._insert_one(entity)

    async def get_student_id_number_by_telegram(self, telegram: str):
        stmt = select(UserEntity.student_id).where(UserEntity.telegram == telegram)
        student_id = await self._select_one(stmt)
        stmt = select(StudentEntity.student_id_number).where(StudentEntity.student_id == student_id)
        return await self._select_one(stmt)
