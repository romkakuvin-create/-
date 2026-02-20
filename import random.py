import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, LabeledPrice, PreCheckoutQuery, SuccessfulPayment

# --- НАСТРОЙКИ ---
API_TOKEN = '8465750252:AAEh4w2Ju7Kwq8ThDVgNjK8wZWLZflkOpVA' 
ADMIN_ID = 12345678 # Вставь свой ID, чтобы работала команда /give
# Если нет своего сайта, пока используй эту тестовую ссылку с колесом:
WEB_APP_URL = "https://roulette-example.vercel.app" 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Имитация базы данных
user_data = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    spins = user_data.get(user_id, 0)
    
    kb = [
        [types.InlineKeyboardButton(text="🎰 Играть в Web-App", web_app=WebAppInfo(url=WEB_APP_URL))],
        [types.InlineKeyboardButton(text="⭐️ Купить попытку (250 XTR)", callback_data="buy_spin")]
    ]
    await message.answer(
        f"У тебя **{spins}** попыток.\nНажми на кнопку, чтобы открыть рулетку!",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=kb),
        parse_mode="Markdown"
    )

# Команда для админа: /give 1234567 5 (ID и кол-во)
@dp.message(Command("give"))
async def admin_give(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        _, uid, count = message.text.split()
        user_data[int(uid)] = user_data.get(int(uid), 0) + int(count)
        await message.answer(f"✅ Начислено {count} попыток юзеру {uid}")
    except:
        await message.answer("Формат: `/give ID кол-во`")

@dp.callback_query(F.data == "buy_spin")
async def pay_spin(callback: types.CallbackQuery):
    await bot.send_invoice(
        callback.message.chat.id,
        title="Пополнение попыток",
        description="1 прокрут рулетки с призами",
        payload="pay_roulette",
        currency="XTR",
        prices=[LabeledPrice(label="1 Спин", amount=250)]
    )

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(F.successful_payment)
async def got_payment(message: types.Message):
    uid = message.from_user.id
    user_data[uid] = user_data.get(uid, 0) + 1
    await message.answer("⭐️ Оплата принята! +1 попытка начислена.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())