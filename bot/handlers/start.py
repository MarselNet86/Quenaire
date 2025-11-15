from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from states.survey import Survey
from keyboards.inline import yes_no_kb
from services.clean_message import send_clean_message

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    # очищаем состояние на всякий случай
    await state.clear()

    # пытаемся удалить команду /start чтобы не засорять переписку
    try:
        await message.delete()
    except:
        pass

    # отправляем первое сообщение пользователю (с авто-удалением предыдущего)
    await send_clean_message(
        state=state,
        chat_id=message.from_user.id,
        bot=message.bot,
        text="Добрый день! Хотите оставить заявку на подключение услуги?",
        reply_markup=yes_no_kb(),
    )

    await state.set_state(Survey.want_service)
