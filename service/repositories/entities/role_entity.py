import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from service.repositories.base.declarative_base import DeclarativeBase


class RoleEntity(DeclarativeBase):
    __tablename__ = 'RoleEntity'

    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    code_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    rules = relationship('RuleEntity', backref='role',
                         lazy='select')
