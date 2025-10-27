from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
import os

# 🔐 BOT TOKEN (Railway'da Environment Variables orqali qo‘shiladi)
BOT_TOKEN = os.getenv("7379852050:AAFaz5l3G3oL735z128qRF-LnLiv5c7yAO8")

# 🔗 Majburiy kanal username (masalan: @my_channel)
CHANNEL = "@kotta_bolacha"

# 🔧 Sozlamalar
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


# 🔍 Kanalga obuna bo‘lganini tekshirish
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False


# 🧠 /start buyrug‘i
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    subscribed = await check_subscription(user_id)

    if subscribed:
        await message.answer("✅ Assalomu alaykum!\nSiz kanalga obuna bo‘lgansiz. Botdan foydalanishingiz mumkin.")
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL[1:]}"))
        keyboard.add(types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_subs"))
        await message.answer("❌ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=keyboard)


# 🔁 “Tekshirish” tugmasi
@dp.callback_query_handler(lambda c: c.data == 'check_subs')
async def check_subs(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    subscribed = await check_subscription(user_id)

    if subscribed:
        await callback.message.edit_text("✅ Rahmat! Siz obuna bo‘ldingiz.\nEndi botdan foydalanishingiz mumkin.")
    else:
        await callback.answer("❌ Hali obuna bo‘lmagansiz!", show_alert=True)


# 🚀 Botni ishga tushirish
if name == 'main':
    asyncio.run(executor.start_polling(dp, skip_updates=True))
