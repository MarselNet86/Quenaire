import aiohttp
from config import API_BASE_URL


async def send_survey(data: dict):
    url = f"{API_BASE_URL}/survey/create/"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            return await resp.json()
