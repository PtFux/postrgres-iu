import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from service.repositories.base.declarative_base import DeclarativeBase


class UsingPromoCodeEntity(DeclarativeBase):
    __tablename__ = 'UsingPromoCodeEntity'

    using_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    student_id = Column(UUID, ForeignKey('StudentEntity.student_id'))
    promo_code_id = Column(UUID, ForeignKey('PromoCodeEntity.promo_code_id'))
