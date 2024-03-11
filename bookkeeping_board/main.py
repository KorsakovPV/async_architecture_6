import asyncio

import uvicorn
from fastapi import FastAPI

import router

app_bookkeeping_board = FastAPI()


@app_bookkeeping_board.get("/")
async def home():
    return "Hello World!"


app_bookkeeping_board.include_router(router=router.router)
asyncio.create_task(router.consume_message())

if __name__ == "__main__":
    # logger.info(f"Start with configuration: \n{app_settings.model_dump()}")
    uvicorn.run("main:app_bookkeeping_board", host="localhost", port=8002)
