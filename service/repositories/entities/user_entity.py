import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from service.repositories.base.declarative_base import DeclarativeBase


class UserEntity(DeclarativeBase):
    __tablename__ = 'UserEntity'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(UUID, ForeignKey('StudentEntity.student_id'))

    telegram = Column(String, nullable=False, unique=True)
    tg_name = Column(String, nullable=True)
    role_code = Column(String, nullable=True)
