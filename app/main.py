from fastapi import FastAPI
from app.crypto.router import router
from app.crypto.scheduler import start_scheduler
from loguru import logger

app = FastAPI()

try:
    scheduler = start_scheduler()
    if scheduler and scheduler.running:
        logger.info("Scheduler успешно запущен")
    else:
        logger.error("Scheduler не запустился")
except Exception as e:
    logger.error(f"Ошибка при запуске scheduler: {e}")

app.include_router(router)
