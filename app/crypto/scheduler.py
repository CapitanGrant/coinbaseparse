from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.crypto.dao import CryptoDAO
from app.crypto.schemas import SCryptoCreate
from app.crypto.services.CryptoDataController import CryptoServices
from loguru import logger

from app.dao.database import async_session_maker


async def scheduled_price_collection():
    """Периодический сбор цен"""
    symbols = CryptoServices.get_all_name_cryptos()
    prices = await CryptoServices.get_prices_and_changes(symbols)
    try:
        async with async_session_maker() as session:
            for symbol, crypto_data in prices.items():
                if crypto_data:
                    try:
                        crypto_create = SCryptoCreate(
                            name=crypto_data["name"],
                            price=crypto_data["price"],
                            dynamic=crypto_data["dynamic"]
                        )
                        await CryptoDAO.add(session=session, values=crypto_create)
                        await session.commit()
                    except Exception as e:
                        print(e)
        print(f"Saved {len(prices)} prices")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await session.close()


def start_scheduler():
    """Запуск планировщика"""
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            scheduled_price_collection,
            'interval',
            hours=0,
            minutes=1,
            coalesce=True,
            id='crypto_price_collection'
        )
        scheduler.start()
        return scheduler
    except Exception as e:
        logger.error(f"Ошибка при запуске планировщика: {e}")
        raise
