import asyncio

import uvicorn
from fastapi import FastAPI

from api.api_router import api_router
from core.config import app_settings
from core.logs import logger
from scheduled_tasks import task_board_scheduler

app_task_board = FastAPI(
    title=app_settings.APP_TITLE,
    description=app_settings.APP_DESCRIPTION,
    version="0.1.0",
    debug=app_settings.DEBUG,
)

app_task_board.include_router(api_router)
asyncio.create_task(task_board_scheduler.main())


if __name__ == "__main__":
    logger.info(f"Start with configuration: \n{app_settings.model_dump()}")
    uvicorn.run("main:app_task_board", host="localhost", port=8001)
