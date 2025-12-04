from telebot import types

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton("📚 Modules"),
            types.KeyboardButton("📝 Enroll"),
            types.KeyboardButton("📊 My Progress"),
            types.KeyboardButton("❓ Help")
        )
        bot.send_message(message.chat.id, "👋 Hello! I'm English Buddy 🤖", reply_markup=markup)
