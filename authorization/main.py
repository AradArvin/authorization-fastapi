from fastapi import FastAPI

from api.api_v1.api import authorization_router


app = FastAPI()


app.include_router(authorization_router, tags=["authorization"], prefix="/authorization")