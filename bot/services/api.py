import aiohttp
from config import API_BASE_URL


async def send_survey(data: dict):
    """
    Отправка анкеты в Django API.
    Функция возвращает (успех: bool, payload: dict | str).
    """
    url = f"{API_BASE_URL}/survey/create/"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as resp:
                # пробуем распарсить тело ответа
                try:
                    payload = await resp.json()
                except Exception:
                    payload = await resp.text()

                # Возвращаем успех, если статус 2xx
                return resp.status < 300, payload

    except aiohttp.ClientError as e:
        # сетевые ошибки: API недоступно, DNS, таймауты и т.п.
        return False, f"Ошибка сети: {e}"

    except Exception as e:
        # любая непредвиденная ошибка
        return False, f"Неизвестная ошибка: {e}"