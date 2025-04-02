from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from langdetect import detect, LangDetectException
import asyncio
import logging

# ✅ توكن البوت
API_TOKEN = "7586933389:AAHV1X_ETWLADqZxDkZq8bUD_Sxuau09PlU"

# ✅ تهيئة البوت والموزع
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ✅ إعدادات تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# ✅ رسالة الترحيب
WELCOME_TEXT = """
📌 NoFarsi Bot – فلترة ذكية للدردشة (@FilterFarsiBot)
🚫 يمنع الرسائل الفارسية تلقائيًا.
✅ يسمح بالعربية وباقي اللغات.
⚙️ يعمل بكفاءة في المجموعات.
🔒 يحافظ على بيئة نقاش مناسبة.
"""

# ✅ أمر /start و /help
@dp.message(Command("start", "help"))
async def send_welcome(message: Message):
    await message.answer(WELCOME_TEXT, parse_mode="Markdown")

# 🚨 تصفية اللغة الفارسية
@dp.message()
async def filter_farsi(message: Message):
    try:
        # تجاهل الأوامر
        if not message.text or message.text.startswith('/'):
            return

        # اكتشاف اللغة
        lang = detect(message.text.strip())

        # حذف الرسائل الفارسية
        if lang == "fa":
            await message.delete()
            warn_msg = await message.answer("⚠️ It's not allowed to type in Farsi here, speak English !\n\يُمنع التحدث بالفارسية هنا ⚠️")
            await asyncio.sleep(5)
            await warn_msg.delete()

    except LangDetectException:
        logging.warning("تعذر تحديد لغة الرسالة")
    except Exception as e:
        logging.error(f"خطأ غير متوقع: {e}")

# ✅ تشغيل البوت
async def main():
    logging.info("✅ البوت قيد التشغيل...")
    await dp.start_polling(bot, skip_updates=True)

if __name__=="__main__":
    asyncio.run(main())