import uuid

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from service.repositories.base.declarative_base import DeclarativeBase


class RatingEntity(DeclarativeBase):
    __tablename__ = 'RatingEntity'

    rating_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(UUID, ForeignKey('StudentEntity.student_id'))

    amount = Column(Integer, nullable=False, default=0)
    last_amount = Column(Integer, nullable=True)
