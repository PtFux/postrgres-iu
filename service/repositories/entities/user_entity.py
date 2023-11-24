import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from service.repositories.base.declarative_base import DeclarativeBase


class UserEntity(DeclarativeBase):
    __tablename__ = 'UserEntity'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    role_id = Column(UUID, ForeignKey('RoleEntity.role_id'))
    student_id = Column(UUID, ForeignKey('StudentEntity.student_id'))

    telegram = Column(String, nullable=False)
    telephone = Column(String, nullable=True)
