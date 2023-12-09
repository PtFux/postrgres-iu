import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from service.repositories.base.declarative_base import DeclarativeBase


class StudentEntity(DeclarativeBase):
    __tablename__ = 'StudentEntity'

    student_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    student_id_number = Column(String, unique=True, index=True, nullable=False)

    rating = relationship('RatingEntity', backref='student',
                          lazy='select')
    contributions = relationship('ContributionEntity', backref='student',
                                 lazy='select')

