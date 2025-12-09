from telebot import types
from others.progress_store import format_progress


def register_handlers(bot):
    @bot.message_handler(commands=["start", "menu"])
    def start_menu(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton("📚 Modules"),
            types.KeyboardButton("📝 Enroll"),
            types.KeyboardButton("📊 My Progress"),
            types.KeyboardButton("❓ Help")
        )

        text = (
            "👋 Welcome to English Buddy!\n"
            "\n"
            "📚 Modules – study vocabulary, grammar and take quizzes.\n"
            "📝 Enroll – register to save your progress.\n"
            "📊 My Progress – check your completed modules and quiz scores.\n"
            "❓ Help – learn how the bot works."
        )

        bot.send_message(message.chat.id, text, reply_markup=markup)


    @bot.message_handler(func=lambda msg: msg.text == "📚 Modules")
    def handle_modules(message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(1, 10):
            markup.add(types.InlineKeyboardButton(f"📘 Module {i}", callback_data=f"module_{i}"))
        bot.send_message(message.chat.id, "📚 Choose a module:", reply_markup=markup)


    # === Обработчик кнопки "My Progress" ===
    @bot.message_handler(func=lambda m: m.text == "📊 My Progress")
    def handle_my_progress(message):
        text = format_progress(message.chat.id)
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    # === Обработчик кнопки "Help" ===
    @bot.message_handler(func=lambda msg: msg.text == "❓ Help")
    def handle_help(message):
        help_text = (
            "📘 *How to Use This Bot*\n\n"
            "📚 *Modules*\n"
            "Study vocabulary, grammar, and take quizzes for each module.\n\n"
            "📝 *Enroll*\n"
            "Register to save your quiz results and track your progress.\n\n"
            "📊 *My Progress*\n"
            "View completed modules and your quiz scores.\n\n"
            "❓ *Quizzes*\n"
            "• Use A/B/C for multiple-choice.\n"
            "• Use T/F for True–False.\n"
            "• Type the correct word for gap-fill tasks.\n\n"
            "⚙ *If something doesn’t work*\n"
            "1) Use /menu to return to the main menu.\n"
            "2) Restart the bot if needed."
        )

        bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
