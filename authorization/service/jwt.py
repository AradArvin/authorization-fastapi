from redis import asyncio as aioredis

from jwt_auth.utils import *
from exception.exception import *
from connection.httpx_manager import httpx_response_mongodb_data


class JWTService:

    HOST_ADDRESS: str = settings.REDIS_HOST_ADDRESS 


    def __init__(self) -> None:
        self.redis = aioredis.from_url(self.HOST_ADDRESS, decode_responses=True)



    async def get_token_user(self, token: str) -> dict:

        token = token.split(" ")[1]

        payload = await token_decode(token)
        user_id = payload["user_id"]

        try:
            await self.get_user_refresh_token(user_id=user_id)
        except:
            raise UserIsNotLoggedInError
        
        user_id_dict = {"id": user_id}
        user = await httpx_response_mongodb_data("api/v1/mongodb", user_id_dict)

        return user
    

