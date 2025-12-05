from telebot import types

# импортируем хранилище прогресса
from others.progress_store import update_stats


# импортируем все викторины
from quizzes.quiz_module_1 import quiz_questions as quiz1_questions
from quizzes.quiz_module_2 import quiz_questions as quiz2_questions
from quizzes.quiz_module_3 import quiz_questions as quiz3_questions
from quizzes.quiz_module_4 import quiz_questions as quiz4_questions
from quizzes.quiz_module_5 import quiz_questions as quiz5_questions
from quizzes.quiz_module_6 import quiz_questions as quiz6_questions
from quizzes.quiz_module_7 import quiz_questions as quiz7_questions
from quizzes.quiz_module_8 import quiz_questions as quiz8_questions
from quizzes.quiz_module_9 import quiz_questions as quiz9_questions

# номер модуля -> список вопросов
QUIZ_DATA = {
    1: quiz1_questions,
    2: quiz2_questions,
    3: quiz3_questions,
    4: quiz4_questions,
    5: quiz5_questions,
    6: quiz6_questions,
    7: quiz7_questions,
    8: quiz8_questions,
    9: quiz9_questions,
}

# user_id -> {"module": int, "index": int, "score": int}
user_progress = {}


def register_handlers(bot):
    # ===== Кнопка "📚 Modules" – показать 9 модулей =====
    @bot.message_handler(func=lambda m: m.text == "📚 Modules")
    def show_modules(message):
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(1, 10):
            markup.add(
                types.InlineKeyboardButton(
                    f"📘 Module {i}", callback_data=f"module_{i}"
                )
            )
        bot.send_message(message.chat.id, "📚 Choose a module:", reply_markup=markup)

    # ===== Выбор модуля: показать опции Vocabulary / Grammar / Quiz =====
    @bot.callback_query_handler(func=lambda call: call.data.startswith("module_"))
    def show_module_options(call):
        module_num = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                "📚 Vocabulary", callback_data=f"vocab_{module_num}"
            )
        )
        markup.add(
            types.InlineKeyboardButton(
                "📖 Grammar", callback_data=f"grammar_{module_num}"
            )
        )
        markup.add(
            types.InlineKeyboardButton(
                "📝 Quiz", callback_data=f"quiz_{module_num}"
            )
        )
        markup.add(
            types.InlineKeyboardButton(
                "◀️ Back to Modules", callback_data="back_to_modules"
            )
        )

        bot.edit_message_text(
            f"📘 Module {module_num} options:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
        )

    # ===== Кнопка "◀️ Back to Modules" =====
    @bot.callback_query_handler(func=lambda call: call.data == "back_to_modules")
    def back_to_modules(call):
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in range(1, 10):
            markup.add(
                types.InlineKeyboardButton(
                    f"📘 Module {i}", callback_data=f"module_{i}"
                )
            )
        bot.edit_message_text(
            "📚 Choose a module:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
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
                parse_mode="html",
            )
        except FileNotFoundError:
            bot.send_message(
                call.message.chat.id,
                f"❌ {action.capitalize()} file for Module {num} not found.",
            )

    # ======== функции для статистики и викторин ========

       def get_questions_for_user(user_id):
        module_num = user_progress[user_id]["module"]
        return QUIZ_DATA.get(module_num, [])

    @bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_"))
    def start_quiz(call):
        user_id = call.from_user.id
        module_num = int(call.data.split("_")[1])

        questions = QUIZ_DATA.get(module_num)
        if not questions:
            bot.send_message(user_id, "❌ Quiz for this module is not ready yet.")
            return

        user_progress[user_id] = {"module": module_num, "index": 0, "score": 0}
        ask_question(user_id)

    def ask_question(user_id):
        questions = get_questions_for_user(user_id)
        index = user_progress[user_id]["index"]

        if index < len(questions):
            # есть следующий вопрос
            question = questions[index]["question"]
            bot.send_message(user_id, f"❓ Question {index + 1}: {question}")
        else:
            # вопросы закончились – сохраняем статистику
            score = user_progress[user_id]["score"]
            module_num = user_progress[user_id]["module"]
            total = len(questions)

            update_stats(user_id, module_num, score, total)

            bot.send_message(
                user_id,
                f"✅ Quiz completed! Your score: {score}/{total}",
            )
            del user_progress[user_id]

    @bot.message_handler(func=lambda message: message.chat.id in user_progress)
    def check_answer(message):
        user_id = message.chat.id
        questions = get_questions_for_user(user_id)
        index = user_progress[user_id]["index"]

        # Защита от выхода за границы
        if index >= len(questions):
            bot.send_message(user_id, "✅ Quiz already finished.")
            # на всякий случай чистим прогресс
            user_progress.pop(user_id, None)
            return

        correct_answer = questions[index]["answer"]
        user_answer = message.text.strip().lower()

        # correct_answer может быть строкой или списком
        if isinstance(correct_answer, list):
            normalized = [str(a).strip().lower() for a in correct_answer]
            is_correct = user_answer in normalized
        else:
            is_correct = user_answer == str(correct_answer).strip().lower()

        if is_correct:
            user_progress[user_id]["score"] += 1
            bot.send_message(user_id, "✅ Correct!")
        else:
            bot.send_message(
                user_id,
                f"❌ Wrong. Correct answer was: {correct_answer}",
            )

        user_progress[user_id]["index"] += 1
        ask_question(user_id)

        user_answer = message.text.strip().lower()

        # correct_answer может быть строкой или списком
        if isinstance(correct_answer, list):
            normalized = [str(a).strip().lower() for a in correct_answer]
            is_correct = user_answer in normalized
        else:
            is_correct = user_answer == str(correct_answer).strip().lower()

        if is_correct:
            user_progress[user_id]["score"] += 1
            bot.send_message(user_id, "✅ Correct!")
        else:
            bot.send_message(
                user_id,
                f"❌ Wrong. Correct answer was: {correct_answer}",
            )

        user_progress[user_id]["index"] += 1
        ask_question(user_id)
