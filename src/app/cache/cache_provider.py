import asyncio
from redis.asyncio.client import PubSub
from starlette.websockets import WebSocket
import redis.asyncio as redis
from pydantic import RedisDsn


class RedisProvider:
    _instance = None
    redis_connection = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dsn:RedisDsn):
        connection_from_url = redis.ConnectionPool.from_url(
            str(dsn),
            decode_responses=True,
        )
        self.redis_connection = redis.Redis(connection_pool=connection_from_url)

    def pubsub(self) -> PubSub:
        return self.redis_connection.pubsub()

    async def listen(self, pubsub: PubSub, websocket: WebSocket):
        """
        Listener seguro que recibe mensajes de Redis y los envía
        por WebSocket, evitando hangs por Redis o WebSocket.
        """
        try:
            async for message in pubsub.listen():
                # Ignorar mensajes irrelevantes
                if message.get("type") != "pmessage":
                    continue

                text_message = message.get("data")
                if text_message is None:
                    continue

                # Stop condition
                if text_message == "stop":
                    break

                # Enviar mensaje al WebSocket con timeout
                try:
                    await asyncio.wait_for(
                        websocket.send_text(text_message),
                        timeout=5
                    )
                except (asyncio.TimeoutError, RuntimeError) as e:
                    break

                # Evitar spin loop
                await asyncio.sleep(0)

        except asyncio.CancelledError:
            raise
        finally:
            try:
                await pubsub.close()
            except Exception as e:
                print(f"[Listener] Error cerrando PubSub: {e}")

    async def close(self):
        """_summary_"""

        await self.redis_connection.close()
