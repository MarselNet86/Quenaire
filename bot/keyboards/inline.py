from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def yes_no_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Да", callback_data="yes")
    kb.button(text="Нет", callback_data="no")
    kb.adjust(2)
    return kb.as_markup()


def client_type_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Я действующий клиент", callback_data="client_old")],
        [InlineKeyboardButton(text="🔵 Я новый клиент", callback_data="client_new")]
    ])



def settlements_kb(top10: list):
    keyboard = []

    # Топ-10 населённых пунктов
    for s in top10:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{s['name']} 🏙",
                callback_data=f"settle_{s['id']}"
            )
        ])

    # Поиск через @бот
    keyboard.append([
        InlineKeyboardButton(
            text="🔎 Найти населённый пункт",
            switch_inline_query_current_chat=""
        )
    ])

    # Ввести вручную
    keyboard.append([
        InlineKeyboardButton(
            text="📝 Ввести свой населённый пункт",
            callback_data="settle_custom"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def house_type_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Частный дом", callback_data="house_private")],
        [InlineKeyboardButton(text="🏢 Квартира", callback_data="house_flat")],
    ])