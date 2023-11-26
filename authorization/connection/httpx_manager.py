import httpx
from core import settings



# HTTP_X requests to other fastapi appes in order to send or recive json data

async def httpx_response(account_endpoint: str, data: dict = None):

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.ACCOUNT_ADDRESS}/{account_endpoint}", json=data)

    return response.json()



async def httpx_response_mongodb_data(data_endpoint: str, data: dict = None):

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.DATA_ADDRESS}/{data_endpoint}", json=data)

    return response.json()



async def httpx_response_mongodb_data_update(data_endpoint: str, data: dict = None):

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.DATA_ADDRESS}/{data_endpoint}", json=data)

    return response.json()