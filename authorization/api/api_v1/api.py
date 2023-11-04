from fastapi import APIRouter, Body, status, HTTPException, Header, Depends, Request
from fastapi.encoders import jsonable_encoder

from schema.token import *
from service.jwt import JWTService
from service.setter import SetterService
from jwt_auth.bearer import JWTBearer
from exception.exception import *
from connection.httpx_manager import httpx_response_mongodb_data_update

authorization_router = APIRouter()



@authorization_router.post(path="/api/v1/signup", summary="User Signup", response_model=Tokens, status_code=status.HTTP_200_OK)
async def user_signup(user_id: dict, 
                      setter_service: SetterService = Depends(),):

    response_data = await setter_service.user_token_setter(user_id.get("id", None))

    return response_data





