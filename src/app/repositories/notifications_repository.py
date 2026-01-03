import asyncio

class NotificationsRepository:

    async def is_alive(self):
        return {"status": "Notifications is alive"}

    async def socket_notifications(self, websocket, channel):
        cache_provider = websocket.app.state.redis

        await websocket.accept()

        pubsub = cache_provider.pubsub()
        await pubsub.psubscribe(channel)

        redis_task = asyncio.create_task(
            cache_provider.listen(pubsub, websocket)
        )

        ws_task = asyncio.create_task(
            self._ws_disconnect_listener(websocket)
        )

        done, pending = await asyncio.wait(
            {redis_task, ws_task},
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    async def _ws_disconnect_listener(self, websocket):
        try:
            while True:
                await websocket.receive()
        except Exception:
            print("[WS] Cliente desconectado")