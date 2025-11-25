from decimal import Decimal

from sqlalchemy import (
    Integer,
    String,
    Float,
    DECIMAL,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.database import Base


class Crypto(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(15, 6), nullable=False)
    dynamic: Mapped[float] = mapped_column(Float, nullable=True)
