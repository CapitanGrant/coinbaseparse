from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class SCryptoBase(BaseModel):
    name: str = Field(description="Cryptocurrency name")
    price: Decimal = Field(description="Cryptocurrency price")
    dynamic: Decimal | None = Field(None, description="Cryptocurrency dynamic")


class SCryptoCreate(SCryptoBase):
    pass


class CryptoHistoryResponse(BaseModel):
    id: int = Field(description="Cryptocurrency id")
    name: str = Field(description="Cryptocurrency symbol")
    price: Decimal = Field(description="Cryptocurrency price rub")
    dynamic: Decimal | None = Field(None, description="Cryptocurrency change_24h")
    created_at: datetime = Field(description="Cryptocurrency creation date")


class CryptoDynamicPoint(BaseModel):
    dynamic: Decimal | None = Field(None, description="Cryptocurrency dynamic")
    price: Decimal | None = Field(None, description="Cryptocurrency price rub")


class CryptoDynamicResponse(BaseModel):
    currency: str = Field(description="Cryptocurrency currency")
    max_dynamic: CryptoDynamicPoint | None = Field(None, description="Cryptocurrency max dynamic")
    min_dynamic: CryptoDynamicPoint | None = Field(None, description="Cryptocurrency min dynamic")
    date_from: date = Field(description="Cryptocurrency date from")
    date_to: date = Field(description="Cryptocurrency date to")
