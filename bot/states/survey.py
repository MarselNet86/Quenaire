from aiogram.fsm.state import StatesGroup, State

class Survey(StatesGroup):
    phone = State()                # получаем телефон
    client_type = State()          # выбор клиент/новый
    settlement = State()           # выбор населённого пункта
    settlement_custom = State()    # ввод своего населённого пункта
    street = State()               # улица
    house = State()                # дом

