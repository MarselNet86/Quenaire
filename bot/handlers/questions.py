from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.survey import Survey
from keyboards.inline import client_type_kb, settlements_kb, house_type_kb
from services.api import ApiClient



router = Router()
api = ApiClient()

# --- 1. Выбор: действующий или новый клиент ---
@router.callback_query(Survey.client_type)
async def choose_client_type(call: CallbackQuery, state: FSMContext):
    if call.data == "client_old":
        # заменяем текст без клавиатуры
        await call.message.edit_text(
            "К сожалению, на данный момент новых предложений для вас нет 🤷‍♂️\n\n"
            "Если захотите пройти опрос — просто нажмите /start 🚀"
        )

        # Здесь вывод FAQ отдельными сообщениями
        await state.clear()
        return

    if call.data == "client_new":
        # сначала меняем текст на "укажите населённый пункт"
        await call.message.edit_text("🏙 Укажите населённый пункт...")

        # получаем топ 10
        success, settlements = await api.get_settlements()
        top10 = settlements[:10]

        # затем обновляем СУЩЕСТВУЮЩЕЕ сообщение с клавой
        await call.message.edit_text(
            "📍 Выберите населённый пункт или введите свой:",
            reply_markup=settlements_kb(top10)
        )

        await state.set_state(Survey.settlement)
        return


# --- 2. Пользователь выбирает населённый пункт ---
@router.callback_query(Survey.settlement)
async def choose_settlement(call: CallbackQuery, state: FSMContext):
    if call.data == "settle_custom":
        await call.message.edit_text(
            "📝 Введите свой населённый пункт:"
        )
        await state.set_state(Survey.settlement_custom)
        return

    settlement_id = int(call.data.replace("settle_", ""))
    await state.update_data(settlement=settlement_id)

    await call.message.edit_text(
        "🚏 Укажите улицу:"
    )
    await state.set_state(Survey.street)


# --- 3. Ввод собственного населённого пункта ---
@router.message(Survey.settlement)
@router.message(Survey.settlement_custom)
async def settlement_text_handler(message: Message, state: FSMContext):
    await state.update_data(settlement_custom=message.text)
    await message.answer("🚏 Укажите улицу:")
    await state.set_state(Survey.street)


# --- 4. Улица ---
@router.message(Survey.street)
async def street_step(message: Message, state: FSMContext):
    await state.update_data(street=message.text)
    await message.answer("🏠 Укажите номер дома:")
    await state.set_state(Survey.house)


# --- 5. Дом ---
@router.message(Survey.house)
async def house_step(message: Message, state: FSMContext):
    await state.update_data(house=message.text)

    await message.answer(
        "Укажите тип жилья:",
        reply_markup=house_type_kb()
    )

    await state.set_state(Survey.house_type)


@router.callback_query(Survey.house_type)
async def choose_house_type(call: CallbackQuery, state: FSMContext):
    if call.data == "house_private":
        # частный дом → квартира не нужна
        await state.update_data(apartment=None)

        await call.message.edit_text("⏳ Отправляю вашу заявку...")

        data = await state.get_data()

        success, resp = await api.check_user(call.from_user.id)
        data['user'] = resp['user']['id']

        success, resp = await api.send_survey(data)

        if not success:
            await call.message.answer(
                "❗ Произошла ошибка при отправке заявки.\n"
                f"<b>{resp}</b>"
            )
            return

        await call.message.answer(
            "🎉 Спасибо! Ваша заявка успешно отправлена!\n"
            "Мы свяжемся с вами в ближайшее время 🙌"
        )
        await state.clear()
        return

    # квартира → спрашиваем номер квартиры
    if call.data == "house_flat":
        await call.message.edit_text("🏢 Укажите номер квартиры:")
        await state.set_state(Survey.apartment)


@router.message(Survey.apartment)
async def apartment_step(message: Message, state: FSMContext):
    await state.update_data(apartment=message.text)

    await message.answer("⏳ Отправляю вашу заявку...")

    data = await state.get_data()

    success, resp = await api.check_user(message.from_user.id)
    data['user'] = resp['user']['id']

    success, resp = await api.send_survey(data)

    if not success:
        await message.answer(
            "❗ Произошла ошибка при отправке заявки.\n"
            f"<b>{resp}</b>"
        )
        return

    await message.answer(
        "🎉 Спасибо! Ваша заявка успешно отправлена!\n"
        "Мы свяжемся с вами в ближайшее время 🙌"
    )

    await state.clear()
