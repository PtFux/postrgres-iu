import uuid

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from service.repositories.base.declarative_base import DeclarativeBase


class PromoCodeEntity(DeclarativeBase):
    __tablename__ = 'PromoCodeEntity'

    promo_code_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    code = Column(String, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False, default=1)
