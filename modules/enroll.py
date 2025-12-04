import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Путь к файлу с ключами:
# 1) на сервере берём из переменной окружения GOOGLE_CREDS_JSON
# 2) локально (на твоём компьютере) можно оставить creds.json
creds_path = os.getenv("GOOGLE_CREDS_JSON", "creds.json")

creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)

sheet = client.open_by_key("14rygWcgNxr8QsGcaEp8YU652V5lPJMVZdUh5SK9j6PA").sheet1


def register_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == "📝 Enroll")
    def handle_enroll(message):
        user_id = message.from_user.id
        name = message.from_user.full_name
        username = message.from_user.username if message.from_user.username else "—"
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        try:
            # Добавляем строку в таблицу
            sheet.append_row([str(user_id), name, f"@{username}", date])
            bot.send_message(message.chat.id, "✅ You are successfully enrolled!")

        except Exception as e:
            bot.send_message(message.chat.id, f"⚠ Error saving to Google Sheets: {e}")