from aiogram.fsm.context import FSMContext




async def send_clean_message(
    state: FSMContext,
    chat_id: int,
    bot,
    text: str,
    reply_markup=None,
):
    """
    Удаляет предыдущее сообщение бота (если есть) и отправляет новое.
    Сохраняет message_id последнего сообщения бота в FSM.
    """
    data = await state.get_data()
    last_id = data.get("last_bot_message_id")

    if last_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=last_id)
        except Exception:
            # сообщение уже могло быть удалено — игнорируем
            pass

    new_msg = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
    )

    await state.update_data(last_bot_message_id=new_msg.message_id)
    return new_msg