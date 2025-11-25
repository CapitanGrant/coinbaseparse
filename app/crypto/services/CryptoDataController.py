import asyncio
from decimal import Decimal
import aiohttp
import requests
from loguru import logger

MAX_CONCURRENT = 4


class CryptoServices:

    @staticmethod
    def get_all_name_cryptos() -> list[str]:
        """Получить список всех доступных криптовалют"""
        r = requests.get("https://api.exchange.coinbase.com/products")
        products = r.json()
        cryptos = sorted({p["base_currency"] for p in products if p["status"] == "online"})
        return cryptos

    @staticmethod
    async def fetch_single_price(session, crypto: str, usd_to_rub: Decimal) -> Decimal | None:
        """Получение цены криптовалюты в RUB"""
        try:
            async with session.get(f"https://api.coinbase.com/v2/prices/{crypto}-USD/spot") as response:
                if response.status == 200:
                    data = await response.json()
                    price_usd = Decimal(data["data"]["amount"])
                    return price_usd * usd_to_rub
        except Exception as e:
            print(f"Ошибка при получении цены для {crypto}: {e}")
            return None

    @staticmethod
    async def fetch_day_change(session, symbol: str, sem: asyncio.Semaphore) -> Decimal | None:
        """Изменение цены за сутки (в %)"""
        symbol = symbol.strip().upper()
        url = f"https://api.exchange.coinbase.com/products/{symbol}-USD/stats"

        try:
            async with sem:
                async with session.get(url) as response:
                    if response.status != 200:
                        return None
                    data = await response.json()
                    if not data or "open" not in data or "last" not in data:
                        return None
                    open_price = Decimal(data["open"])
                    last_price = Decimal(data["last"])
                    if open_price == 0:
                        return None
                    return (last_price - open_price) / open_price * 100
        except Exception as e:
            logger.error(f"Неожиданная ошибка для {symbol}-USD: {e}", exc_info=True)
            return None

    @staticmethod
    async def _get_usd_to_rub_rate(session) -> Decimal:
        """Получить курс USD к RUB"""
        try:
            async with session.get("https://api.exchangerate-api.com/v4/latest/USD") as response:
                data = await response.json()
                return Decimal(str(data["rates"]["RUB"]))
        except Exception as e:
            logger.error(f"Не удалось получить курс RUB: {e}", exc_info=True)
            return Decimal("90.0")

    @staticmethod
    async def get_prices_and_changes(cryptos: list[str]) -> dict:
        async with aiohttp.ClientSession() as session:
            sem = asyncio.Semaphore(MAX_CONCURRENT)
            usd_to_rub = await CryptoServices._get_usd_to_rub_rate(session)
            price_tasks = [
                CryptoServices.fetch_single_price(session, crypto, usd_to_rub)
                for crypto in cryptos
            ]
            change_tasks = [
                CryptoServices.fetch_day_change(session, crypto, sem)
                for crypto in cryptos
            ]

            prices = await asyncio.gather(*price_tasks)
            changes = await asyncio.gather(*change_tasks)

            result = {}
            for crypto, price, change in zip(cryptos, prices, changes):
                if price is not None:
                    result[crypto] = {
                        "name": crypto,
                        "price": price,
                        "dynamic": change
                    }

            return result
