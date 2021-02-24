from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types.message import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp
from Db import Db, VolDb
from binance_def import alphab_lists, get_price, tickers_list
import sqlite3
from states import Key

db = sqlite3.connect('database.sqlite', check_same_thread=False)

#start
@dp.message_handler(CommandStart( ))
async def bot_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🧮Calculate entry volume")
    item2 = types.KeyboardButton("⚙Configure API Key⚙")
    markup.add(item1, item2)  # добавляем кнопку на клавиатуре
    await message.answer(f"Hi, {message.from_user.full_name}!\nThis bot is designed to calculate the volume of entry into a trade on BinanceFutures. If you want to start, click on the '🧮Calculate entry volume' button and then follow the instructions.\nWe wish you a profitable trade💰!", reply_markup=markup)
#first_keyboard
@dp.message_handler(Text(equals=['⚙Configure API Key⚙', '🧮Calculate entry volume']))
async def first_keyboard(message):
    if message.chat.type == 'private':
        if message.text == '⚙Configure API Key⚙':
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            item3 = types.KeyboardButton("📝Insert API keys")
            item4 = types.KeyboardButton("❌Delete API keys")
            item5 = types.KeyboardButton("↩Back to main menu")
            markup2.add(item3, item4, item5)
            await message.answer(f"{message.from_user.full_name}, choose the button", reply_markup=markup2)
        elif message.text == '🧮Calculate entry volume':
            # выводим буквы
            markup = types.InlineKeyboardMarkup(row_width=4)

            item3 = types.InlineKeyboardButton("1...", callback_data='1')
            item4 = types.InlineKeyboardButton("A...", callback_data='A')
            item5 = types.InlineKeyboardButton("B...", callback_data='B')
            item6 = types.InlineKeyboardButton("C...", callback_data='C')
            item7 = types.InlineKeyboardButton("D...", callback_data='D')
            item8 = types.InlineKeyboardButton("E...", callback_data='E')
            item9 = types.InlineKeyboardButton("F...", callback_data='F')
            item10 = types.InlineKeyboardButton("G...", callback_data='G')
            item11 = types.InlineKeyboardButton("H...", callback_data='H')
            item12 = types.InlineKeyboardButton("I...", callback_data='I')
            item13 = types.InlineKeyboardButton("J...", callback_data='J')
            item14 = types.InlineKeyboardButton("K...", callback_data='K')
            item15 = types.InlineKeyboardButton("L...", callback_data='L')
            item16 = types.InlineKeyboardButton("M...", callback_data='M')
            item17 = types.InlineKeyboardButton("N...", callback_data='N')
            item18 = types.InlineKeyboardButton("O...", callback_data='O')
            item19 = types.InlineKeyboardButton("P...", callback_data='P')
            item20 = types.InlineKeyboardButton("Q...", callback_data='Q')
            item21 = types.InlineKeyboardButton("R...", callback_data='R')
            item22 = types.InlineKeyboardButton("S...", callback_data='S')
            item23 = types.InlineKeyboardButton("T...", callback_data='T')
            item24 = types.InlineKeyboardButton("U...", callback_data='U')
            item25 = types.InlineKeyboardButton("V...", callback_data='V')
            item26 = types.InlineKeyboardButton("W...", callback_data='W')
            item27 = types.InlineKeyboardButton("X...", callback_data='X')
            item28 = types.InlineKeyboardButton("Y...", callback_data='Y')
            item29 = types.InlineKeyboardButton("Z...", callback_data='Z')
            markup.add(item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13, item14, item15,
                       item16, item17, item18, item19, item20, item21, item22, item23, item24, item25, item26, item27,
                       item28, item29)
            await message.answer('Choose the first letters of your asset:', reply_markup=markup)

### работа с блоком "апи"

@dp.message_handler(Text(equals=['📝Insert API keys']))
async def first_keyboard(message):
    if message.chat.type == 'private':
        if message.text == '📝Insert API keys':
            await message.answer(
                f"{message.from_user.full_name}, Insert Your API_KEY:\n(with 'Api: ' at the beginning of the message)\nFormat:\nApi: Your_Api_Key")
            await Key.Q1.set( )


@dp.message_handler(Text(equals=['❌Delete API keys', '↩Back to main menu']))
async def first_keyboard(message):
    if message.chat.type == 'private':
        if message.text == '❌Delete API keys':
            h = message.from_user.id
            a = Db(db)
            a.destroy(h)
            await message.answer("Okey, deletion successful")
        elif message.text == '↩Back to main menu':
            markups = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item11 = types.KeyboardButton("🧮Calculate entry volume")
            item21 = types.KeyboardButton("⚙Configure API Key⚙")
            markups.add(item11, item21)  # добавляем кнопку на клавиатуре
            await message.answer(
                f"Hi, {message.from_user.full_name}!\nThis bot is designed to calculate the volume of entry into a trade on BinanceFutures. If you want to start, click on the '🧮Calculate entry volume' button and then follow the instructions.\nWe wish you a profitable trade💰!",
                reply_markup=markups)

#вставляем апи ключ (возможно убрать работу с текстом?)
@dp.message_handler(state=Key.Q1)
async def api_key(Apimessage: types.Message, state: FSMContext):
    try:
        apiKey = Apimessage
        key = (apiKey["text"][-64:])
        h = Apimessage.from_user.id
        c = Db(db)
        c.insert_user_id(h)
        a = Db(db)
        a.insert_api_key(key, h)
        await state.update_data(answer1=apiKey)
        await Apimessage.answer(
            "Okey, Insert Your Secret_Key:")
        await Key.Q2.set( )
    except Exception:
        await Apimessage.answer(
            "Error. Delete keys and try again")
        await state.finish( )

#вставляем секретный ключ
@dp.message_handler(state=Key.Q2)
async def sec_key(Secmessage, state: FSMContext):
    try:
        secKey = Secmessage
        skey = (secKey["text"][-64:])
        h = Secmessage.from_user.id
        a = Db(db)
        a.insert_secret_key(skey, h)
        data = await state.get_data( )
        answer1 = data.get("answer1")
        answer2 = secKey
        await Secmessage.answer("Okey, Keys added successfully!")
        await state.finish( )
    except Exception:
        await Secmessage.answer(
            "Error. Delete keys and try again")
        await state.finish()

###работа с блоком активов
# выдаем список активов по выбранной букве либо цену актива
@dp.callback_query_handler(lambda callback_query: True)
async def callback_letter(call):
    if call.message:
        alph = ['1', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                'U', 'V', 'W', 'X', 'Y', 'Z']
        tickersList = tickers_list([])
        if call.data in alph:
            #чистим базу
            h = call.message.chat.id
            a = VolDb(db)
            a.destroy(h)
            list1 = alphab_lists(call.data)
            keyboard_symb = types.InlineKeyboardMarkup(row_width=2)
            for symb in list1:
                keyboard_symb.add(types.InlineKeyboardButton(text=symb, callback_data=symb))
            await call.message.answer('Choose your asset:', reply_markup=keyboard_symb)

        elif call.data in tickersList:
            ticker = call.data
            print(ticker)
            user_id = call.from_user.id
            c = VolDb(db)
            c.insert_user_id_vol(user_id)
            a = VolDb(db)
            a.insert_ticker(ticker, user_id)
            price = get_price(call.data)
            b = VolDb(db)
            b.insert_price(price, user_id)
            resetBut = types.ReplyKeyboardMarkup(resize_keyboard=True)
            DelBut = types.KeyboardButton("❌Reset token settings")
            back = types.KeyboardButton("↩Back to main menu")
            resetBut.add(DelBut, back)
            await call.message.answer(
                f"{call.data} сurrent price - {price},\nInsert Your risk per trade in $:\n(with a sign '$' at the end).\nFor example: 10$ or 10.5$",
                reply_markup=resetBut)
            # return price

# удаление данных для расчета
@dp.message_handler(Text(equals=['❌Reset token settings']))
async def first_keyboard(message):
    if message.chat.type == 'private':
        h = message.from_user.id
        a = VolDb(db)
        a.destroy(h)
        backBut = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("↩Back to main menu")
        backBut.add(back)
        await message.answer("Okey, reset successful", reply_markup=backBut)

# расчет объема
@dp.message_handler(Text(endswith='$'))
async def dollar_risk(message):
    try:
        risk_dollar = message.text
        dollar = risk_dollar.replace("$", "")
        user_id = message.from_user.id
        b = VolDb(db)
        b.insert_dollar(dollar, user_id)
        await message.answer("Insert Your risk per trade in %:\n(with a sign '%' at the end).\nFor example: 2% or 2.5%")
        return dollar
    except TypeError:
        await message.answer(
            "Wrong format. You must enter a number in the format [number]$\n(for example: 6$ or 6.5$)")
    except Exception:
        await message.answer(
            "Error. Reset token settings and try again.")


@dp.message_handler(Text(endswith='%'))
async def perc_risk(message):
    try:
        risk_perc = message.text
        percent = risk_perc.replace("%", "")
        user_id = message.from_user.id
        b = VolDb(db)
        b.insert_percent(percent, user_id)
        vol = VolDb(db)
        v = vol.all(message.from_user.id)
        print(v)
        await message.answer(f"Successful!\nYour volume - {v}")
        return risk_perc
    except TypeError:
        await message.answer(
            "Wrong format. You must enter a number in the format [number]%\n(for example: 2% or 2.5%)")
    except Exception:
        await message.answer(
            "Error. Reset token settings and try again.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


