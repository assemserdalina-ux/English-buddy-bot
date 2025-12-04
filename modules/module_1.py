from telebot import types
from quizzes.quiz_module_1 import quiz_questions


def register_handlers(bot):
    # ===== Кнопка "📚 Modules" – показать 9 модулей =====
    @bot.message_handler(func=lambda m: m.text == "📚 Modules")
    def show_modules(message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(1, 10):
            markup.add(types.InlineKeyboardButton(f"📘 Module {i}", callback_data=f"module_{i}"))
        bot.send_message(message.chat.id, "📚 Choose a module:", reply_markup=markup)

    # ===== Выбор модуля: показать опции Vocabulary / Grammar / Quiz =====
    @bot.callback_query_handler(func=lambda call: call.data.startswith("module_"))
    def show_module_options(call):
        module_num = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📚 Vocabulary", callback_data=f"vocab_{module_num}"))
        markup.add(types.InlineKeyboardButton("📖 Grammar", callback_data=f"grammar_{module_num}"))
        markup.add(types.InlineKeyboardButton("📝 Quiz", callback_data=f"quiz_{module_num}"))
        markup.add(types.InlineKeyboardButton("◀️ Back to Modules", callback_data="back_to_modules"))

        bot.edit_message_text(
            f"📘 Module {module_num} options:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # ===== Кнопка "◀️ Back to Modules" =====
    @bot.callback_query_handler(func=lambda call: call.data == "back_to_modules")
    def back_to_modules(call):
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(1, 10):
            markup.add(types.InlineKeyboardButton(f"📘 Module {i}", callback_data=f"module_{i}"))
        bot.edit_message_text(
            "📚 Choose a module:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # ===== Vocabulary / Grammar из файлов (БЕЗ quiz_!) =====
    @bot.callback_query_handler(func=lambda call: call.data.startswith(("vocab_", "grammar_")))
    def show_module_content(call):
        action, num = call.data.split("_")
        filename = f"text/module_{num}/{action}.txt"

        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            title = {
                "vocab": "📚 Vocabulary",
                "grammar": "📖 Grammar",
            }.get(action, "📄 Content")

            bot.send_message(
                call.message.chat.id,
                f"<b>{title}</b>\n\n{content}",
                parse_mode='html'
            )
        except FileNotFoundError:
            bot.send_message(
                call.message.chat.id,
                f"❌ {action.capitalize()} file for Module {num} not found."
            )

    # ====== ИНТЕРАКТИВНАЯ ВИКТОРИНА ДЛЯ MODULE 1 ======
    # Храним прогресс викторины по пользователям
    user_progress = {}

    # Запуск викторины по нажатию "📝 Quiz" в Module 1
    @bot.callback_query_handler(func=lambda call: call.data == "quiz_1")
    def start_quiz(call):
        user_id = call.from_user.id
        user_progress[user_id] = {"index": 0, "score": 0}
        bot.send_message(user_id, "📝 Quiz for Module 1. Type your answers in the chat.")
        ask_question(user_id)

    # Задаём вопрос по текущему индексу
    def ask_question(user_id):
        index = user_progress[user_id]["index"]
        if index < len(quiz_questions):
            question = quiz_questions[index]["question"]
            bot.send_message(user_id, f"❓ Question {index + 1}: {question}")
        else:
            score = user_progress[user_id]["score"]
            bot.send_message(
                user_id,
                f"✅ Quiz completed! Your score: {score}/{len(quiz_questions)}"
            )
            # очищаем прогресс
            del user_progress[user_id]

    # Проверка ответа пользователя
    @bot.message_handler(func=lambda message: message.chat.id in user_progress)
    def check_answer(message):
        user_id = message.chat.id
        index = user_progress[user_id]["index"]
        correct_answer = quiz_questions[index]["answer"]

        if message.text.strip().lower() == correct_answer.strip().lower():
            user_progress[user_id]["score"] += 1
            bot.send_message(user_id, "✅ Correct!")
        else:
            bot.send_message(user_id, f"❌ Wrong. Correct answer was: {correct_answer}")

        user_progress[user_id]["index"] += 1
        ask_question(user_id)
