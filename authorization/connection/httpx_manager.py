import httpx
from core import settings



async def httpx_response(account_endpoint: str, data: dict = None):

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.ACCOUNT_ADDRESS}/{account_endpoint}", json=data)

    return response.json()


