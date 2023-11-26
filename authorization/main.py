from fastapi import FastAPI

from api.api_v1.api import authorization_router


# Create the fastapi app
app = FastAPI()

# Including routes in app 
app.include_router(authorization_router, tags=["authorization"], prefix="/authorization")