from aiogram.fsm.state import StatesGroup, State

class Survey(StatesGroup):
    want_service = State()
    street = State()
    house = State()
    name = State()
    phone = State()
    current_services = State()
