import uuid

from sqlalchemy import Column, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from service.repositories.base.declarative_base import DeclarativeBase


class ContributionEntity(DeclarativeBase):
    __tablename__ = 'ContributionEntity'

    contribution_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    amount = Column(SmallInteger, nullable=False, default=0)
    season = Column(SmallInteger, nullable=False)
    year = Column(SmallInteger, nullable=False)
    status = Column(SmallInteger, nullable=False)

    student_id = Column(UUID, ForeignKey('StudentEntity.student_id'))

