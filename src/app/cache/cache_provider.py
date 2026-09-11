import asyncio
import json  # Importar la biblioteca json

import redis.asyncio as redis
from pydantic import RedisDsn
from redis.asyncio.client import PubSub, Redis
from starlette.websockets import WebSocket


class RedisProvider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dsn: RedisDsn):
        self.dsn = dsn
        self.redis_connection = None
        self.connect()

    def connect(self):
        """Establish a connection to the Redis server."""
        if self.redis_connection is not None:
            print("Redis connection already established.")
            return

        try:
            connection_from_url = redis.ConnectionPool.from_url(
                str(self.dsn),
                decode_responses=True,
            )
            self.redis_connection = Redis(connection_pool=connection_from_url)
            print(f"Connected to Redis at {self.dsn}")
        except Exception as e:
            print(f"[RedisProvider] Error connecting to Redis: {e}")

    def pubsub(self) -> PubSub:
        """Create a new PubSub object for the current connection."""
        if self.redis_connection is None:
            raise ValueError("Redis connection not established.")
        return self.redis_connection.pubsub()

    async def listen(self, pubsub: PubSub, websocket: WebSocket):
        """
        Listener seguro que recibe mensajes de Redis y los envía
        por WebSocket, evitando hangs por Redis o WebSocket.
        """
        if self.redis_connection is None:
            raise ValueError("Redis connection not established.")

        try:
            async for message in pubsub.listen():
                # Ignorar mensajes irrelevantes
                if message.get("type") != "pmessage":
                    continue

                text_message = message.get("data")
                if text_message is None:
                    print("[RedisProvider] Received empty message.")
                    continue

                # Stop condition
                if text_message == "stop":
                    break

                try:
                    # Deserializar el mensaje JSON recibido
                    obj_message = json.loads(text_message)
                except json.JSONDecodeError as e:
                    print(f"[RedisProvider] Error decoding JSON: {e}")
                    continue

                # Enviar mensaje al WebSocket con timeout
                try:
                    await asyncio.wait_for(
                        websocket.send_text(
                            json.dumps(obj_message)
                        ),  # Serializar el objeto antes de enviarlo
                        timeout=5,
                    )
                except (asyncio.TimeoutError, RuntimeError) as e:
                    print(f"[RedisProvider] Error sending message to WebSocket: {e}")
                    break

                # Evitar spin loop
                await asyncio.sleep(0)

        except asyncio.CancelledError:
            raise
        finally:
            try:
                await pubsub.close()
            except Exception as e:
                print(f"[RedisProvider] Error closing PubSub: {e}")

    async def close(self):
        """Close the Redis connection."""
        if self.redis_connection is not None:
            try:
                await self.redis_connection.close()
                print("Redis connection closed.")
            except Exception as e:
                print(f"[RedisProvider] Error closing Redis connection: {e}")
            finally:
                self.redis_connection = None
