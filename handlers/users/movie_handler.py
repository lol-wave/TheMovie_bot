from asyncio import timeout
from datetime import datetime
from aiogram.types import InputTextMessageContent, InlineQueryResultCachedVideo, InlineQueryResultCachedDocument
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler

import keyboards.default.delete
from data.config import ADMINS
from keyboards.inline.admin import keyboard, settings, ad_menu
from loader import dp, kino_db, user_db,bot
from aiogram import types
from states.states import KinoAddState, DeleteState, EditCap
from aiogram.types import CallbackQuery



hafta_movies = kino_db.get_movies_hafta()
oy_movies = kino_db.get_movies_oy()

@dp.message_handler(commands='admin')
async def user_count(message:types.Message):
    if str(message.from_user.id)==ADMINS[0]:
        await message.answer(text='.',reply_markup=keyboard)
    else:
        await message.answer("Siz admin emassiz.")
@dp.callback_query_handler(text='today')
async def bugun_stat(call:CallbackQuery):
    if kino_db.get_movies_bugun():
        bugun = kino_db.get_movies_bugun()
        for movie in bugun:
            await call.message.answer(movie+"\n")
    else:
        await call.message.answer("Bugungi kinolar yo'q")
@dp.callback_query_handler(text="week")
async def week_stat(call:CallbackQuery):
    if kino_db.get_movies_hafta():
        for movie in hafta_movies:
            await call.message.answer(movie)
    else:
        await call.message.answer("Bu haftada kinolar yo'q")
@dp.callback_query_handler(text='month')
async def month_stat(call:CallbackQuery):
    if kino_db.get_movies_oy():
        for movie in oy_movies:
            await call.message.answer(movie)
    else:
        await call.message.answer("Bu oyda kinolar yo'q")

@dp.callback_query_handler(text='stats')
async def statistika(call:CallbackQuery):
    await call.message.delete()
    count = user_db.count_users()
    await call.message.answer(f"Bazada <b>{count}</b>  ta foydalanuvchi bor")
from aiogram import types
from aiogram.types import CallbackQuery


stop = False

@dp.callback_query_handler(text='ad')
async def reklama(call: CallbackQuery):
    if str(call.message.from_user.id) in ADMINS:
        await call.message.answer("Reklama yuborilmaydi, adminlar uchun.")
        return

    await call.message.delete()
    await call.message.answer("Reklama videosi yoki rasmini yoziv bilan yuboring.")

    @dp.message_handler(content_types=['photo', 'video', 'text'])
    async def handle_ad_message(ad_message: types.Message):
        global stop  # Use the global stop flag
        not_sent = 0
        sent = 0
        admins = 0
        text = f"Xabar yuborish\nYuborilgan: {sent}\nYuborilmagan: {not_sent}\nUmumiy: 0/{user_db.count_users()}\n\nStatus: Boshlanmoqda"
        status_message = await ad_message.answer(text, reply_markup=ad_menu)
        users = user_db.select_all_user_ids()

        for user_id in users:
            if str(user_id) in ADMINS:
                not_sent += 1
                admins += 1
                continue

            try:
                await ad_message.forward(user_id)
                sent += 1
            except:
                not_sent += 1

            text = f"Xabar yuborish\nYuborilgan: {sent}\nYuborilmagan: {not_sent} ({admins}ta Admin)\nUmumiy: {sent + not_sent}/{user_db.count_users()}\nStatus: Davom etmoqda"
            await bot.edit_message_text(text, chat_id=ad_message.chat.id, message_id=status_message.message_id, reply_markup=ad_menu)

            if stop:
                text11 = f"Xabar yuborish\nYuborilgan: {sent}\nYuborilmagan: {not_sent} ({admins}ta Admin)\nUmumiy: {sent + not_sent}/{user_db.count_users()}\nStatus: To'xtatildi"
                stop = False
                await bot.edit_message_text(text11,chat_id=ad_message.chat.id,message_id=status_message.message_id)
                await ad_message.answer("To'xtatildi.")
                raise CancelHandler

        text = f"Xabar yuborish\nYuborilgan: {sent}\nYuborilmagan: {not_sent} ({admins}ta Admin)\nUmumiy: {user_db.count_users()}/{user_db.count_users()}\nStatus: Tugadi"
        await bot.edit_message_text(text, chat_id=ad_message.chat.id, message_id=status_message.message_id)

@dp.callback_query_handler(text='pause_ad')
async def stop_ad(call: CallbackQuery):
    global stop
    stop = True
    raise CancelHandler
@dp.callback_query_handler(text='admin_menu_ad')
async def back_from_ad(call:CallbackQuery):
    global stop
    stop = True
    await call.message.delete()
    await call.message.answer("To'xtatildi",reply_markup=keyboard)
    raise CancelHandler






@dp.callback_query_handler(text='count_movie')
async def counting(call: CallbackQuery):
    counter = kino_db.count_kino()
    if counter and counter[0] > 0:
        await call.message.delete()
        await call.message.answer(f"Bazada <b>{counter[0]}</b> ta kino bor")
    else:
        await call.message.delete()
        await call.message.answer("Bazada kino yo'q")


@dp.callback_query_handler(text='movie_settings')
async def switching(call:CallbackQuery):
    await call.message.delete()
    await call.message.answer(".",reply_markup=settings)

@dp.callback_query_handler(text='admin_menu')
async def admin_panel(call:CallbackQuery):
    await call.message.delete()
    await call.message.answer(".",reply_markup=keyboard)

@dp.callback_query_handler(text='add_movie')
async def kino_add_func(call:CallbackQuery):
    await call.message.delete()
    if str(call.from_user.id) in ADMINS:
        await KinoAddState.kino_add.set()
        await call.message.answer("Kino va kinoning nomini yuboring")
    else:
        await call.message.answer("Siz admin emassiz")

@dp.message_handler(state=KinoAddState.kino_add, content_types=types.ContentType.VIDEO)
async def message_kino_added(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['file_id'] = message.video.file_id
    post_id = kino_db.generate_unique_post_id()
    try:
        name=message.caption
        # caption1=f" Kino nomi: {name}\n\n"
        # caption1+=f"Kino kodi: {post_id}"
        # caption1+=f"Kiritilgan vaqt: {datetime.now()}\n"
        # caption1+=f"Eng zo'r va zamonaviy kinolar @TheUzb_Movies_bot da"

    except:
        await message.answer("Xatolik")
        await state.finish()
        return
    await state.update_data(nameo=name,ido=post_id,fid=data['file_id'])
    # kino_db.add_movie(post_id, data['file_id'],name,caption1)
    # await message.reply(f"Kino {post_id} kod bilan muvaffaqqiyatli yuklandi")
    await message.answer("Capiton yuboring")
    await KinoAddState.caption.set()
@dp.message_handler(state=KinoAddState.caption)
async def cap(message:types.Message,state:FSMContext):
    now=datetime.now()
    date_only_str = now.strftime("%Y-%m-%d")
    await state.update_data(captiono=message.text)
    datap=await state.get_data()
    name=datap['nameo']
    idp=datap['ido']
    file=datap['fid']
    captionp=datap['captiono']
    caption1=f" Kino nomi: {name}\n\n"
    caption1+=f"Kino kodi: {idp}\n\n"
    caption1+=captionp+"\n\n"
    caption1+=f"Kiritilgan kun: {date_only_str}\n"
    caption1+=f"Eng zo'r va zamonaviy kinolar @TheUzb_Movies_bot da"
    kino_db.add_movie(idp, file,name,caption1)
    await message.answer(f"Kino {idp} kod bilan muvaffaqqiyatli yuklandi")
    await state.finish()



@dp.callback_query_handler(text='delete_movie')
async def delete_movie_handler(call:CallbackQuery):
    if str(call.from_user.id) in ADMINS:
        await call.message.delete()
        await call.message.answer("Post IDni yuboring")
        await DeleteState.kutish.set()
    else:
        await call.message.delete()
        await call.message.answer("Siz admin emassiz")

@dp.message_handler(state=DeleteState.kutish)
async def wait_for_delete_id(message: types.Message, state: FSMContext):
    try:
        post_id = int(message.text)
        await state.update_data(post=post_id)
    except ValueError:
        await message.answer("Iltimos, to'g'ri post ID kiriting.")
        await state.finish()
        return
    if kino_db.get_movie_by_post_id(post_id):
        await message.answer("Kinoni o'chirmoqchimisiz?",reply_markup=keyboards.default.delete.conifirm)
        await DeleteState.confirmation.set()
    else:
        await message.answer("Kino topilmadi. O'chirish uchun berilgan post ID mavjud emas.")
        await state.finish()

@dp.message_handler(text="Ha",state=DeleteState.confirmation)
async def tanlov(message:types.Message,state:FSMContext):
    data1=await state.get_data()
    pst_id=int(data1['post'])
    kino_db.delete_movie(pst_id)
    await message.answer(f"{pst_id} koddagi kino muvaffaqqiyatli o'chirildi",reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

@dp.message_handler(text="Yo'q",state=DeleteState.confirmation)
async def tanlov(message:types.Message,state:FSMContext):
    await message.answer("Bekor qilindi",reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

@dp.callback_query_handler(text='edit_caption')
async def update_cap(call:CallbackQuery):
    if str(call.from_user.id) in ADMINS:
        await call.message.delete()
        await call.message.answer("Post IDni kiriting")
        await EditCap.ID.set()
    else:
        await call.message.delete()
        await call.message.answer("Siz admin emassiz")
@dp.message_handler(state=EditCap.ID)
async def getid(message:types.Message, state:FSMContext):
    try:
        post_id=int(message.text)
        await state.update_data({'pst_id':post_id})

        await message.answer("Captionni kiriting")
        await EditCap.caption.set()
    except ValueError:
        await message.answer("Iltimos, to'g'ri post ID kiriting.")
        await state.finish()
@dp.message_handler(state=EditCap.caption)
async def caption(message:types.message,state:FSMContext):
    datao=await state.get_data()

    caption1=message.text
    if kino_db.get_movie_by_post_id(datao['pst_id']):
        kino_db.update_kino_caption(caption1,datao['pst_id'])
        await message.answer("Caption muvaffaqiyatli o'zgartirildi")
        await state.finish()
    else:
        await message.answer("Bu kino mavjud emas")
        await state.finish()


@dp.inline_handler()
async def inline_video(query: types.InlineQuery):
    movie_name = query.query.strip()

    file_id = kino_db.get_movie_by_name(movie_name)

    if file_id:
        results = [
            InlineQueryResultCachedDocument(
                id=str(hash(movie_name)),
                document_file_id=file_id['file_id'],
                title=file_id['nameo'],
                caption=file_id['caption'],
                parse_mode="html",
            )
        ]
        # Send the inline results
        await query.answer(results)
    else:
        await query.answer([])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






