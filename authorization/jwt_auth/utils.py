from datetime import datetime, timedelta
from bson.objectid import ObjectId
import jwt
import uuid

from core import settings



def gen_jti():
    """Generate hexed unique jti for user"""
    return str(uuid.uuid4().hex)

jti = gen_jti()


async def create_access_token(user_id: str) -> str: 
    return await _create_token(token_type="access", 
                         lifetime=settings.ACCESS_TOKEN_EXPIRE_MINUTES, 
                         time_unit=settings.ACCESS_TOKEN_TIME_UNIT, 
                         user_id=user_id, 
                         jti=jti)


async def create_access_token_from_refresh(user_id: str, ref_token_payload: dict) -> str: 
    expire = await token_exp_time(settings.ACCESS_TOKEN_TIME_UNIT, settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    if expire > datetime.utcfromtimestamp(int(ref_token_payload["exp"])):
        expire = datetime.utcfromtimestamp(int(ref_token_payload["exp"]))

    token_jti = ref_token_payload["jti"]

    return await _create_token(token_type="access", 
                         user_id=user_id, 
                         jti=token_jti,
                         expire=expire)


async def create_refresh_token(user_id: str) -> str: 
    return await _create_token(token_type="refresh", 
                         lifetime=settings.REFRESH_TOKEN_EXPIRE_MINUTES, 
                         time_unit=settings.REFRESH_TOKEN_TIME_UNIT, 
                         user_id=user_id, 
                         jti=jti)





