iimport time
import logging
import traceback
import os
import telebot

try:
    from Token_bot.token_bot import Token as LOCAL_TOKEN
except ImportError:
    LOCAL_TOKEN = None

BOT_TOKEN = os.getenv("BOT_TOKEN") or LOCAL_TOKEN

if not BOT_TOKEN:
    raise RuntimeError("Bot token is not set. Set BOT_TOKEN env var or LOCAL_TOKEN.")

bot = telebot.TeleBot(BOT_TOKEN)

from menu import menu
from modules import module_1, enroll


logging.basicConfig(level=logging.INFO)

def register_all_handlers(bot):
    menu.register_handlers(bot)
    module_1.register_handlers(bot)
    enroll.register_handlers(bot)


if __name__ == "__main__":
    while True:
        try:
            register_all_handlers(bot)
            logging.info("✅ Bot is running...")
            bot.infinity_polling(timeout=30, long_polling_timeout=30)

        except Exception as e:
            logging.error("❌ Unexpected error occurred:")
            traceback.print_exc()
        time.sleep(5)