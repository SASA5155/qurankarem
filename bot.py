import asyncio
import aiosqlite
import datetime
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8520176300:AAEU1qoEmP2Nn1Fu8_CYicS3jbgF016fN_8"
ADMIN_ID = 5166153612
DB_PATH = 'quran_bot.db'
DEFAULT_TZ = pytz.timezone("Africa/Cairo")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(bot)

# Database init
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER UNIQUE,
            lang TEXT DEFAULT 'ar',
            enabled_ayah INTEGER DEFAULT 1,
            enabled_hadith INTEGER DEFAULT 1,
            enabled_azkar_morning INTEGER DEFAULT 1,
            enabled_azkar_evening INTEGER DEFAULT 1,
            enabled_daily_recap INTEGER DEFAULT 1,
            enabled_audio INTEGER DEFAULT 1
        )
        """)
        await db.commit()

# Start command
@dp.message(Command("start"))
async def start_cmd(msg: types.Message):
    if msg.from_user.id == ADMIN_ID:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('➕ إضافة قناة', callback_data='add_ch')],
            [InlineKeyboardButton('📢 القنوات', callback_data='list_ch')],
            [InlineKeyboardButton('⏰ ضبط الأوقات', callback_data='times')]
        ])
        await msg.answer("لوحة تحكم المشرف", reply_markup=kb)
    else:
        await msg.answer("بوت نشر تلقائي للقرآن والأذكار")

# المزيد من Handlers مثل add_channel, auto_poster... (كما في الكود السابق)

async def main():
    await init_db()
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())

