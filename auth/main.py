import uvicorn
from fastapi import FastAPI

from api.api_router import api_router
from core.config import app_settings
from core.logs import logger

app_auth = FastAPI(
    title=app_settings.APP_TITLE,
    description=app_settings.APP_DESCRIPTION,
    version="0.1.0",
    debug=app_settings.DEBUG,
)

app_auth.include_router(api_router)


if __name__ == "__main__":
    logger.info(f"Start with configuration: \n{app_settings.model_dump()}")
    uvicorn.run("main:app_auth", host="localhost", port=8000)
