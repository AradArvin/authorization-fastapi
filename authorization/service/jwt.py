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
    

    async def get_user_refresh_token(self, user_data: dict = None, user_id: str = None) -> str:
        """
        returns the refresh_token if the cached key is not timed out.
        If it's timedout then the user needs to login again
        """

        if user_data:
            uid = f"user_{user_data['id']}"
            id = user_data['id']
        elif user_id:
            uid = f"user_{user_id}"
            id = user_id

        all_keys = await self.redis.keys("*")
        for i in all_keys:
            x = i.split(" ")
            if uid == x[0]:
                exp = await self.redis.get(i)
                u_uid = x[1]

            return await self.recreate_refresh_token(id, exp, u_uid)


    

