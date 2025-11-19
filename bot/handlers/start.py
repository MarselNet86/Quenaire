from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from states.survey import Survey
from keyboards.inline import client_type_kb
from keyboards.reply import request_phone_kb
from services.api import ApiClient


router = Router()
api = ApiClient()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    # Проверка пользователя
    status, data = await api.check_user(message.from_user.id)

    # Если юзер НЕ существует → просим отправить контакт
    if not data.get("exists"):
        await message.answer(
            "Чтобы продолжить, отправьте номер телефона:",
            reply_markup=request_phone_kb()
        )
        await state.set_state(Survey.phone)  # ждём номер
        return
    
    # Если юзер есть и телефон есть → начинаем опрос
    await message.answer(
        "Добрый день!\n\n"
        "Вы действующий клиент или новый клиент?",
        reply_markup=client_type_kb(),
    )
    await state.set_state(Survey.client_type)



@router.message(Survey.phone)
async def phone_received(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Пожалуйста, нажмите кнопку для отправки номера.")
        return

    phone = message.contact.phone_number

    # Регистрируем пользователя сразу с телефоном
    await api.register_user(
        user=message.from_user,
        phone=phone
    )

    await message.answer(
        "📱 Спасибо! Номер успешно сохранён.",
        reply_markup=ReplyKeyboardRemove(),
    )

    await message.answer(
        "Пожалуйста, выберите 👇\n\n"
        "Вы действующий клиент или новый клиент?",
        reply_markup=client_type_kb(),
    )


    await state.set_state(Survey.client_type)
