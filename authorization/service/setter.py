from redis import asyncio as aioredis

from jwt_auth.utils import *
from exception.exception import *



class SetterService:

    HOST_ADDRESS: str = settings.REDIS_HOST_ADDRESS

    def __init__(self) -> None:
        self.redis = aioredis.from_url(self.HOST_ADDRESS, decode_responses=True)



    async def user_token_setter(self, user_id: ObjectId):
        access_token = await create_access_token(user_id)
        refresh_token = await create_refresh_token(user_id)

        refresh_token_payload = await token_decode(refresh_token)
        
        await self.key_setter(refresh_token_payload)

        response_data = {
            "access": access_token,
            "refresh": refresh_token,
        }

        return response_data
    


