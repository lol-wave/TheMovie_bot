from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

conifirm=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ha"),
            KeyboardButton(text="Yo'q")
        ],

    ],
    resize_keyboard=True
)