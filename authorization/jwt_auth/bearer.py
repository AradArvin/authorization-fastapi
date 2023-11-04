from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import token_decode
import jwt



# Bearer Token
class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True, is_refresh: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.is_refresh = is_refresh


    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if await self.verify_jwt(credentials.credentials) == "invalid":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token!")
            if await self.verify_jwt(credentials.credentials) == "expired":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is expired!")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code.")



