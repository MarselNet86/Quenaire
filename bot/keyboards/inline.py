from aiogram.utils.keyboard import InlineKeyboardBuilder


def yes_no_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Да", callback_data="yes")
    kb.button(text="Нет", callback_data="no")
    kb.adjust(2)
    return kb.as_markup()


def services_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Мобильная связь", callback_data="mobile")
    kb.button(text="Медный телефон", callback_data="copper")
    kb.adjust(1)
    return kb.as_markup()
