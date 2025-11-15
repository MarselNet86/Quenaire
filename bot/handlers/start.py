from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.survey import Survey
from keyboards.inline import yes_no_kb
from services.clean_message import send_clean_message

router = Router()   # <<< ВАЖНО — именно этого не хватало


@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear()

    # можно удалить саму команду /start, чтобы чат был чище
    try:
        await message.delete()
    except Exception:
        pass

    await send_clean_message(
        state=state,
        chat_id=message.from_user.id,
        bot=message.bot,
        text="Добрый день! Хотите оставить заявку на подключение услуги?",
        reply_markup=yes_no_kb(),
    )

    await state.set_state(Survey.want_service)