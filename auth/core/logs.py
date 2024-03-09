import logging
from logging.config import dictConfig

from core.config import app_settings

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s[%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %Z",
        },
    },
    "handlers": {
        "console": {
            "level": app_settings.LOG_LEVEL,
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "root": {
            "level": app_settings.LOG_LEVEL,
            "handlers": ["console"],
        }
    },
}

# Initiate logger config
dictConfig(LOGGER_CONFIG)
logger = logging.getLogger("root")
