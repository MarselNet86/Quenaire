from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.survey import Survey
from keyboards.inline import yes_no_kb, services_kb
from services.api import send_survey
from services.clean_message import send_clean_message

router = Router()


# --- 1. Ответ "Да" ---
@router.callback_query(Survey.want_service, F.data == "yes")
async def ask_street(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except:
        pass

    await send_clean_message(
        state=state,
        chat_id=call.from_user.id,
        bot=call.bot,
        text="Укажите улицу:",
    )

    await state.set_state(Survey.street)


# --- 2. Ответ "Нет" ---
@router.callback_query(Survey.want_service, F.data == "no")
async def cancel(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except:
        pass

    await send_clean_message(
        state=state,
        chat_id=call.from_user.id,
        bot=call.bot,
        text="Хорошо, обращайтесь 😊",
    )

    await state.clear()


# --- 3. Улица ---
@router.message(Survey.street)
async def street_step(message: Message, state: FSMContext):
    try:
        await message.delete()
    except:
        pass

    await state.update_data(street=message.text)

    await send_clean_message(
        state=state,
        chat_id=message.from_user.id,
        bot=message.bot,
        text="Укажите номер дома:",
    )

    await state.set_state(Survey.house)


# --- 4. Дом ---
@router.message(Survey.house)
async def house_step(message: Message, state: FSMContext):
    try:
        await message.delete()
    except:
        pass

    await state.update_data(house=message.text)

    await send_clean_message(
        state=state,
        chat_id=message.from_user.id,
        bot=message.bot,
        text="Ваше имя:",
    )

    await state.set_state(Survey.name)


# --- 5. Имя ---
@router.message(Survey.name)
async def name_step(message: Message, state: FSMContext):
    try:
        await message.delete()
    except:
        pass

    await state.update_data(name=message.text)

    await send_clean_message(
        state=state,
        chat_id=message.from_user.id,
        bot=message.bot,
        text="Ваш номер телефона:",
    )

    await state.set_state(Survey.phone)


# --- 6. Телефон ---
@router.message(Survey.phone)
async def phone_step(message: Message, state: FSMContext):
    try:
        await message.delete()
    except:
        pass

    await state.update_data(phone=message.text)

    await send_clean_message(
        state=state,
        chat_id=message.from_user.id,
        bot=message.bot,
        text="Какие услуги у вас сейчас есть?",
        reply_markup=services_kb(),
    )

    await state.set_state(Survey.current_services)


# --- 7. Завершение ---
@router.callback_query(Survey.current_services)
async def finish(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except:
        pass

    await state.update_data(current_services=call.data)
    data = await state.get_data()

    # отправляем в Django API
    await send_survey(data)

    # финальное сообщение
    await send_clean_message(
        state=state,
        chat_id=call.from_user.id,
        bot=call.bot,
        text="Спасибо! Ваша заявка отправлена 🙌\nМы свяжемся с вами при необходимости."
    )

    await state.clear()
