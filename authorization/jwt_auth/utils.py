from datetime import datetime, timedelta
from bson.objectid import ObjectId
import jwt
import uuid

from core import settings


# Main utility functions used in token generation.


def gen_jti():
    """Generate hexed unique jti for user"""
    return str(uuid.uuid4().hex)

jti = gen_jti()


async def create_access_token(user_id: str) -> str: 
    return await _create_token(token_type="access", 
                         lifetime=settings.ACCESS_TOKEN_EXPIRE, 
                         time_unit=settings.ACCESS_TOKEN_TIME_UNIT, 
                         user_id=user_id, 
                         jti=jti)


async def create_access_token_from_refresh(user_id: str, ref_token_payload: dict) -> str: 
    """
    Gets data from a refresh token payload for logged in user in order to create a new 
    access token for the said user. 
    """
    expire = await token_exp_time(settings.ACCESS_TOKEN_TIME_UNIT, settings.ACCESS_TOKEN_EXPIRE)

    if expire > datetime.utcfromtimestamp(int(ref_token_payload["exp"])):
        expire = datetime.utcfromtimestamp(int(ref_token_payload["exp"]))

    token_jti = ref_token_payload["jti"]

    return await _create_token(token_type="access", 
                         user_id=user_id, 
                         jti=token_jti,
                         expire=expire)


async def create_refresh_token(user_id: str) -> str: 
    return await _create_token(token_type="refresh", 
                         lifetime=settings.REFRESH_TOKEN_EXPIRE, 
                         time_unit=settings.REFRESH_TOKEN_TIME_UNIT, 
                         user_id=user_id, 
                         jti=jti)



async def token_exp_time(time_unit: str, lifetime: int):
    """
    A method to choose the time unit for token ttl. the time unit is set in settings. 
    """
    if time_unit == "seconds":
        expire = datetime.utcnow() + timedelta(seconds=lifetime)
    elif time_unit == "minutes":
        expire = datetime.utcnow() + timedelta(minutes=lifetime)
    elif time_unit == "hours":
        expire = datetime.utcnow() + timedelta(hours=lifetime)
    elif time_unit == "days":
        expire = datetime.utcnow() + timedelta(days=lifetime)
    
    return expire


async def _create_token(token_type: str, user_id: str, jti: str, lifetime: int = None, time_unit: str = None, expire = None) -> str:
    """
    Main function that creates the token.
    """
    payload = dict()
    if not expire:
        exp = await token_exp_time(time_unit, lifetime)
    else:
        exp = expire
    payload["type"] = token_type
    payload["user_id"] = str(user_id)
    payload["exp"] = exp 
    payload["iat"] = datetime.utcnow() 
    payload["jti"] = jti

    return await token_encode(payload)



async def token_encode(payload: dict):
    """
    Encode tokens based on HS256 algorithm
    """

    token = jwt.encode(payload=payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token



async def token_decode(token: str):
    """
    Dencode tokens based on HS256 algorithm
    """

    payload = jwt.decode(jwt=token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    return payload



