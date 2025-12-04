from telebot import types
from modules import module_1, module_2  # ... add up to module_9

def register_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("open_module_"))
    def module_callback(call):
        module_number = call.data.split("_")[-1]
        handler_func = globals().get(f"module_{module_number}")
        if handler_func:
            handler_func.register_handlers(bot)
            handler_func.show_module_menu(bot, call.message)
