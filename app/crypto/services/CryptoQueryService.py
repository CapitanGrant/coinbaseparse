from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.crypto.dao import CryptoDAO
from app.crypto.schemas import CryptoHistoryResponse, CryptoDynamicResponse, CryptoDynamicPoint


class CryptoQueryService:

    @staticmethod
    async def get_all_crypto_history(
            session: AsyncSession,
            date_from: date,
            date_to: date
    ) -> list[CryptoHistoryResponse]:

        prices = await CryptoDAO.get_history(
            session=session,
            date_from=date_from,
            date_to=date_to
        )

        return [
            CryptoHistoryResponse(
                id=p.id,
                name=p.name,
                price=p.price,
                dynamic=p.dynamic,
                created_at=p.created_at,
            )
            for p in prices
        ]

    @staticmethod
    async def get_currency_history(
            session: AsyncSession,
            currency: str,
            date_from: date,
            date_to: date
    ) -> list[CryptoHistoryResponse]:
        try:
            prices = await CryptoDAO.get_currency_history(
                session=session,
                currency=currency,
                date_from=date_from,
                date_to=date_to
            )

            return [
                CryptoHistoryResponse(
                    id=p.id,
                    name=p.name,
                    price=p.price,
                    dynamic=p.dynamic,
                    created_at=p.created_at
                )
                for p in prices
            ]

        except Exception as e:
            logger.error(f"Ошибка при получении истории валюты {currency}: {e}")
            raise

    @staticmethod
    async def get_currency_dynamic_range(
            session: AsyncSession,
            currency: str,
            date_from: date,
            date_to: date
    ) -> CryptoDynamicResponse:
        """Получить максимальную и минимальную дневную динамику."""
        try:
            currency = currency.upper()

            max_dyn = await CryptoDAO.get_max_dynamic(
                session=session,
                currency=currency,
                date_from=date_from,
                date_to=date_to
            )

            min_dyn = await CryptoDAO.get_min_dynamic(
                session=session,
                currency=currency,
                date_from=date_from,
                date_to=date_to
            )

            if not max_dyn or not min_dyn:
                raise ValueError(
                    f"Нет данных по валюте {currency} за указанный период"
                )

            return CryptoDynamicResponse(
                currency=currency,
                max_dynamic=CryptoDynamicPoint(
                    created_at=max_dyn.created_at,
                    dynamic=max_dyn.dynamic,
                    price=max_dyn.price,
                ),
                min_dynamic=CryptoDynamicPoint(
                    created_at=min_dyn.created_at,
                    dynamic=min_dyn.dynamic,
                    price=min_dyn.price,
                ),
                date_from=date_from,
                date_to=date_to,
            )

        except Exception as e:
            logger.error(
                f"Ошибка при получении динамики валюты {currency}: {e}"
            )
            raise
