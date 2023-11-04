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


    

    async def recreate_refresh_token(self, user_id, exp, u_uid):
        """Recreate the cached refresh token."""

        refresh_token = await token_encode({
            'token_type':'refresh',
            'user_id':user_id,
            'exp': exp,
            'iat': datetime.utcnow(),
            'jti':u_uid
        })
        
        return refresh_token



    async def check_user_token(self, user_data: dict):
        token = await self.get_user_refresh_token(user_data=user_data)

        if token is None:
            return
        
        try:
            await token_decode(token)
        except jwt.exceptions.ExpiredSignatureError:
            return "expired"
        


    async def token_deleter(self, user_data: dict):
        """Checkes if a user has refresh token and then deletes it."""

        uid = f"user_{user_data['id']}"
        all_keys = await self.redis.keys("*")
        for i in all_keys:
            x = i.split(" ")
            if uid == x[0]:
                await self.redis.delete(i)



    async def create_access_from_refresh(self, auth_token: str, user_token: str, user_data: dict):
        auth_token = auth_token.split(" ")[1]

        auth_token_payload = await token_decode(auth_token)
        user_refresh_payload = await token_decode(user_token)

        if auth_token_payload["user_id"] != auth_token_payload["user_id"] and auth_token_payload["jti"] != auth_token_payload["jti"]:
            raise InvalidTokenError

        access_token = await create_access_token_from_refresh(user_id=user_data["id"], ref_token_payload=user_refresh_payload)

        return access_token
