from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram import Router
from services.api import ApiClient


router = Router()
api = ApiClient()


@router.inline_query()
async def inline_settlement_search(query: InlineQuery):
    text = query.query.lower().strip()

    if not text:
        return

    # грузим все населённые пункты
    success, settlements = await api.get_settlements()

    filtered = [
        s for s in settlements
        if text in s["name"].lower()
    ][:25]

    results = []

    # 👉 если ничего не нашли — показываем сообщение «нет результатов»
    if not filtered:
        results.append(
            InlineQueryResultArticle(
                id="no-results",
                title="❌ Ничего не найдено",
                description="Такого населённого пункта пока нет в базе",
                input_message_content=InputTextMessageContent(
                    message_text=f"{query.query} (нет в списке)"
                )
            )
        )

        await query.answer(results, cache_time=1)
        return

    # 👉 если есть совпадения — показываем их
    for s in filtered:
        results.append(
            InlineQueryResultArticle(
                id=str(s["id"]),
                title=s["name"],
                description="Населённый пункт",
                input_message_content=InputTextMessageContent(
                    message_text=s["name"]
                )
            )
        )

    await query.answer(results, cache_time=1)

