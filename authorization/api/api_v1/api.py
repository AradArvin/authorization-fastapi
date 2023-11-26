from fastapi import APIRouter, status, HTTPException, Depends, Request
from starlette.responses import JSONResponse


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
    """
    Signup route get's the user_id in a dictionary from account app and creates the user jwt token using
    setter service dependency methods. and then return's the jwt tokens in response. 
    """

    response_data = await setter_service.user_token_setter(user_id.get("id", None))

    return response_data




@authorization_router.post(path="/api/v1/login", summary="User Login", response_model=Tokens, status_code=status.HTTP_200_OK)
async def user_login(user: dict,
                     token_service: JWTService = Depends(),
                     setter_service: SetterService = Depends()):
    """
    Login route get's the user data in a dictionary from account app and creates the user jwt token using
    setter service dependency methods. and then return's the jwt tokens in response. tokens are checked 
    by the token service dependency.
    """

    if await token_service.check_user_token(user) == "expired":
        await token_service.token_deleter(user)

    
    response_data = await setter_service.user_token_setter(user["id"])

    return response_data




@authorization_router.post("/api/v1/profile", dependencies=[Depends(JWTBearer())], summary="See user profile",response_model=UserProfile, status_code=status.HTTP_200_OK)
async def user_profile(request: Request, token_service: JWTService = Depends()):
    """
    Profile route first check's the access token in header by the high level dependency JWTBearer 
    and then the token is used to get user data, which is returned in response.
    """

    token = request.headers.get("Authorization")

    user = await token_service.get_token_user(token)

    return user




@authorization_router.put("/api/v1/update-profile", dependencies=[Depends(JWTBearer())], summary="Update user profile", response_model=UpdateProfile, status_code=status.HTTP_200_OK)
async def update_user_profile(request: Request, 
                              entered_data: dict,
                              token_service: JWTService = Depends()):
    """
    Update profile route check's the accesss token in header by the high level dependency JWTBearer 
    and then user data is updated in mongodb collection. 
    """
    
    token = request.headers.get("Authorization")


    user_data = await token_service.get_token_user(token)

    data = {"user_data": user_data, "entered_data": entered_data}

    updated_user_data = await httpx_response_mongodb_data_update("api/v1/mongodb-update", data)

    return updated_user_data




@authorization_router.post("/api/v1/access-token", dependencies=[Depends(JWTBearer(is_refresh=True))], summary="Get new acess token", status_code=status.HTTP_200_OK)
async def get_access(request: Request, 
                    token_service: JWTService = Depends()):
    
    """
    Access token route check's the refresh token in header by the high level dependency JWTBearer
    and then creates an access token for the user and then returnes a response containing
    the new access token.
    """
    
    auth_token = request.headers.get("Authorization")

    try:
        user_data = await token_service.get_token_user(auth_token)
    except UserIsNotLoggedInError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not logged in")

    try:
        user_refresh_token = await token_service.get_user_refresh_token(user_data)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    

    try:
        access_token = await token_service.create_access_from_refresh(auth_token, user_refresh_token, user_data)
        response_data = {
            "access": access_token,
        }
        return response_data
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token!")




@authorization_router.post("/api/v1/logout", dependencies=[Depends(JWTBearer())], summary="User Log out", status_code=status.HTTP_200_OK)
async def logout(request: Request, 
                 token_service: JWTService = Depends()):
    
    """
    Logout route check's the refresh token in header by the high level dependency JWTBearer
    and then attempts to logout user by deleting the refresh token for user.
    """
    
    token = request.headers.get("Authorization")

    user_data = await token_service.get_token_user(token)

    await token_service.token_deleter(user_data)

    return {"detail": "logged out!"}



@authorization_router.post(path="/api/v1/check-login", summary="check if user is logged in")
async def check_login(request: Request,
                     token_service: JWTService = Depends(),):
    
    """
    Checks if a user has refresh token in redis so is logged in.
    """
    
    token = request.headers.get("Authorization")

    user_data = await token_service.get_token_user(token)

    if user_data.get("id", None) != None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "logged_in"})
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "not_logged_in"})