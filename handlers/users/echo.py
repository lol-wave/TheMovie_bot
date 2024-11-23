from aiogram import types
from aiogram.dispatcher.handler import CancelHandler

from states.states import Search
from aiogram import types
from loader import dp,kino_db,user_db
from aiogram.dispatcher import FSMContext
import logging
from data.config import ADMINS

@dp.message_handler()
async def wait_for_post_id(message: types.Message):
    try:
        kino_kod = int(message.text)
    except ValueError:
        await message.reply("Siz kino kodi yubormadingiz.\nKino kodi raqamdan iborat.")
        raise CancelHandler
    kino = kino_db.get_movie_by_post_id(kino_kod)
    if kino:
        file_id = kino['file_id']
        caption=kino_db.get_movie_cap_by_id(kino_kod)
        if str(message.from_user.id) in ADMINS:
            await message.answer_video(file_id,caption=caption,protect_content=False)
        else:
            await message.answer_video(file_id,caption=caption,protect_content=True)

    else:
        await message.answer("Kino topilmadi.")
        raise CancelHandler
