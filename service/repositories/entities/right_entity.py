import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from service.repositories.base.declarative_base import DeclarativeBase


class RightEntity(DeclarativeBase):
    __tablename__ = 'RightEntity'

    right_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
