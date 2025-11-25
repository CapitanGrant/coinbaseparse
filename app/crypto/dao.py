from datetime import date, datetime, time
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.dao.base import BaseDAO
from app.crypto.models import Crypto


class CryptoDAO(BaseDAO[Crypto]):
    model = Crypto

    @staticmethod
    def _normalize_dates(date_from: date, date_to: date) -> tuple[datetime, datetime]:
        dt_from = datetime.combine(date_from, time.min)
        dt_to = datetime.combine(date_to, time.max)
        return dt_from, dt_to

    @classmethod
    async def get_history(
            cls,
            session: AsyncSession,
            date_from: date,
            date_to: date
    ) -> Sequence[Crypto]:
        """История всех валют."""
        dt_from, dt_to = cls._normalize_dates(date_from, date_to)

        stmt = (
            select(cls.model)
            .where(
                and_(
                    cls.model.created_at >= dt_from,
                    cls.model.created_at <= dt_to
                )
            )
            .order_by(cls.model.created_at.desc())
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_currency_history(
            cls,
            session: AsyncSession,
            currency: str,
            date_from: date,
            date_to: date
    ) -> Sequence[Crypto]:
        """История конкретной валюты."""

        dt_from, dt_to = cls._normalize_dates(date_from, date_to)

        stmt = (
            select(cls.model)
            .where(
                and_(
                    cls.model.name == currency.upper(),
                    cls.model.created_at >= dt_from,
                    cls.model.created_at <= dt_to,
                )
            )
            .order_by(cls.model.created_at.desc())
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_max_dynamic(
            session: AsyncSession,
            currency: str,
            date_from: date,
            date_to: date
    ) -> Crypto | None:
        """Элемент с максимальной дневной динамикой"""
        stmt = (
            select(Crypto)
            .where(
                and_(
                    Crypto.name == currency,
                    Crypto.created_at >= datetime.combine(date_from, datetime.min.time()),
                    Crypto.created_at <= datetime.combine(date_to, datetime.max.time()),
                    Crypto.dynamic.is_not(None)
                )
            )
            .order_by(Crypto.dynamic.desc())
            .limit(1)
        )

        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def get_min_dynamic(
            session: AsyncSession,
            currency: str,
            date_from: date,
            date_to: date
    ) -> Crypto | None:
        """Элемент с минимальной дневной динамикой"""
        stmt = (
            select(Crypto)
            .where(
                and_(
                    Crypto.name == currency,
                    Crypto.created_at >= datetime.combine(date_from, datetime.min.time()),
                    Crypto.created_at <= datetime.combine(date_to, datetime.max.time()),
                    Crypto.dynamic.is_not(None)
                )
            )
            .order_by(Crypto.dynamic.asc())
            .limit(1)
        )

        res = await session.execute(stmt)
        return res.scalar_one_or_none()
