import aiohttp
from config import API_BASE_URL


class ApiClient:
    def __init__(self):
        self.base_url = API_BASE_URL.rstrip("/")

    async def post(self, endpoint: str, json: dict):
        url = f"{self.base_url}{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=json) as resp:
                    try:
                        payload = await resp.json()
                    except Exception:
                        payload = await resp.text()

                    return resp.status < 300, payload
        except aiohttp.ClientError as e:
            return False, f"Ошибка сети: {e}"
        except Exception as e:
            return False, f"Неизвестная ошибка: {e}"

    async def get(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        payload = await resp.json()
                    except Exception:
                        payload = await resp.text()

                    return resp.status < 300, payload
        except aiohttp.ClientError as e:
            return False, f"Ошибка сети: {e}"
        except Exception as e:
            return False, f"Неизвестная ошибка: {e}"

    # ------------------------------
    # Методы API
    # ------------------------------

    async def check_user(self, user_id: int):
        return await self.post("/user/check/", {"user_id": user_id})
    
    async def register_user(self, user, phone):
        payload = {
            "user_id": user.id,
            "full_name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
            "username": user.username,
            "phone_number": phone,
        }
        return await self.post("/user/register/", payload)


    async def get_settlements(self):
        return await self.get("/settlements/")

    async def send_survey(self, data: dict):
        return await self.post("/survey/create/", data)
