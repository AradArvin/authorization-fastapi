from fastapi import APIRouter, Body, status, HTTPException, Header, Depends, Request
from fastapi.encoders import jsonable_encoder

from schema.token import *
from service.jwt import JWTService
from service.setter import SetterService
from jwt_auth.bearer import JWTBearer
from exception.exception import *
from connection.httpx_manager import httpx_response_mongodb_data_update

authorization_router = APIRouter()



