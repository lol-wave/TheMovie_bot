from aiogram.dispatcher.filters.state import StatesGroup,State


class KinoAddState(StatesGroup):
    kino_add=State()
    name=State()
    caption=State()


class DeleteState(StatesGroup):
    kutish = State()
    confirmation=State()

class Search(StatesGroup):
    waiting=State()

class EditCap(StatesGroup):
    ID=State()
    caption=State()

class SearchName(StatesGroup):
    waiting=State()
