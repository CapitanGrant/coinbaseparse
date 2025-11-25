from datetime import date
from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crypto.schemas import (
    CryptoHistoryResponse,
    CryptoDynamicResponse,
)
from app.crypto.services.CryptoQueryService import CryptoQueryService
from app.dao.session_maker import SessionDep

router = APIRouter(prefix="/crypto", tags=["Crypto"])


@router.get("/", summary="Получение истории курса всех валют", response_model=List[CryptoHistoryResponse])
async def get_all_crypto_history(
        dateFrom: date = Query(..., description="Дата забора данных от"),
        dateTo: date = Query(..., description="Дата забора данных до"),
        session: AsyncSession = SessionDep
):
    """Получить историю курсов всех криптовалют за указанный период"""
    try:
        return await CryptoQueryService.get_all_crypto_history(
            session=session,
            date_from=dateFrom,
            date_to=dateTo
        )
    except ValueError as e:
        logger.warning(f"Некорректные параметры запроса: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при получении истории всех валют: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера") from e


@router.get("/{currency}", summary="Получение истории курса конкретной валюты",
            response_model=List[CryptoHistoryResponse])
async def get_currency_history(
        currency: str,
        dateFrom: date = Query(..., description="Дата забора данных от"),
        dateTo: date = Query(..., description="Дата забора данных до"),
        session: AsyncSession = SessionDep
):
    """Получить историю курса конкретной криптовалюты за указанный период"""
    try:
        return await CryptoQueryService.get_currency_history(
            session=session,
            currency=currency.upper(),
            date_from=dateFrom,
            date_to=dateTo
        )
    except ValueError as e:
        logger.warning(f"Некорректные параметры запроса: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при получении истории валюты {currency}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера") from e


@router.get("/dynamic/{currency}", summary="Получение экстремальных значений динамики",
            response_model=CryptoDynamicResponse)
async def get_currency_dynamic_range(
        currency: str,
        dateFrom: date = Query(..., description="Дата забора данных от"),
        dateTo: date = Query(..., description="Дата забора данных до"),
        session: AsyncSession = SessionDep
):
    """Получить время, когда дневная динамика была максимальной и минимальной"""
    try:
        return await CryptoQueryService.get_currency_dynamic_range(
            session=session,
            currency=currency.upper(),
            date_from=dateFrom,
            date_to=dateTo
        )
    except ValueError as e:
        logger.warning(f"Некорректные параметры запроса: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Ошибка при получении динамики валюты {currency}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера") from e
