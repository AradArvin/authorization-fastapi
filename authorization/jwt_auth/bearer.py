from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import token_decode
import jwt



# Bearer Token
class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True, is_refresh: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.is_refresh = is_refresh



