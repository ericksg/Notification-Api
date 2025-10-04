from fastapi import FastAPI, Depends
from starlette.websockets import WebSocket

from src.core.config import settings
from src.core.lifespan import lifespan
from src.cache.cache_provider import RedisProvider

import asyncio

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.get("/isAlive")
async def root():
    return {"status": "Notifications is alive"}


@app.websocket("/ws")
async def ws_root(websocket: WebSocket):
    await websocket.accept()

    cache = RedisProvider(settings.REDIS_DSN)

    pubsub = cache.pubsub()

    await pubsub.psubscribe(settings.NOTIFICATION_CHANNEL)

    async def listen_ws():
        while True:
            message = await websocket.receive_text()
            await pubsub.publish("test_channel", message)

    listener_task = asyncio.create_task(cache.listen(pubsub, websocket))
    other_task = asyncio.create_task(listen_ws())

    done, pending = await asyncio.wait(
        [listener_task, other_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    # Cancel the remaining task
    for task in pending:
        task.cancel()

    await websocket.close()