from redis import asyncio as aioredis

from jwt_auth.utils import *
from exception.exception import *



class SetterService:

    HOST_ADDRESS: str = settings.REDIS_HOST_ADDRESS

    def __init__(self) -> None:
        self.redis = aioredis.from_url(self.HOST_ADDRESS, decode_responses=True)


