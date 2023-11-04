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




@authorization_router.post(path="/api/v1/login", summary="User Login", response_model=Tokens, status_code=status.HTTP_200_OK)
async def user_login(user: dict,
                     token_service: JWTService = Depends(),
                     setter_service: SetterService = Depends()):
    

    if await token_service.check_user_token(user) == "expired":
        await token_service.token_deleter(user)

    
    response_data = await setter_service.user_token_setter(user["id"])

    return response_data




@authorization_router.post("/api/v1/profile", dependencies=[Depends(JWTBearer())], summary="See user profile",response_model=UserProfile, status_code=status.HTTP_200_OK)
async def user_profile(request: Request, token_service: JWTService = Depends()):
    token = request.headers.get("Authorization")

    user = await token_service.get_token_user(token)

    return user




@authorization_router.put("/api/v1/update-profile", dependencies=[Depends(JWTBearer())], summary="Update user profile", response_model=UpdateProfile, status_code=status.HTTP_200_OK)
async def update_user_profile(request: Request, 
                              entered_data: UpdateProfile = Body(),
                              token_service: JWTService = Depends()):
    
    token = request.headers.get("Authorization")

    entered_data = jsonable_encoder(entered_data)

    user_data = await token_service.get_token_user(token)

    data = {"user_data": user_data, "entered_data": entered_data}

    updated_user_data = await httpx_response_mongodb_data_update("api/v1/mongodb-update", data)

    return updated_user_data





