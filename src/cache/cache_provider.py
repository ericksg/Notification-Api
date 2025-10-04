import redis.asyncio as redis

from pydantic import RedisDsn
from redis.client import PubSub
from starlette.websockets import WebSocket


class RedisProvider:
    _instance = None
    redis_connection_pool = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, dsn:RedisDsn):
        connection_from_url = redis.ConnectionPool.from_url(
            str(dsn),
            decode_responses=True,
        )
        self.redis_connection_pool = redis.Redis(connection_pool=connection_from_url)



    def pubsub(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        return self.redis_connection_pool.pubsub()

    async def pubsub_subscribe(self, channel:str):
        pubsub = self.pubsub()

        await pubsub.psubscribe(channel)

    async def listen(self, pubsub: PubSub, websocket: WebSocket):
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is None or message.get('type') != 'pmessage':
                continue
            text_message = message['data']
            if text_message == "stop":
                #await websocket.send_text("closing the connection")
                break
            await websocket.send_text(text_message)

    async def publish(self, channel, message):
        """_summary_

        Args:
            channel (_type_): _description_
            message (_type_): _description_

        Returns:
            _type_: _description_
        """

        return await self.redis_connection_pool.publish(channel, str(message))

    async def close(self):
        """_summary_"""

        await self.redis_connection_pool.close()
