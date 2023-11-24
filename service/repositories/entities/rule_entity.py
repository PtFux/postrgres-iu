import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from service.repositories.base.declarative_base import DeclarativeBase


class RuleEntity(DeclarativeBase):
    __tablename__ = 'RuleEntity'

    rule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    role_id = Column(UUID, ForeignKey('RoleEntity.role_id'))
    right_id = Column(UUID, ForeignKey('RightEntity.right_id'))
