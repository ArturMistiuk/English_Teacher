import telebot
from message_handler import handle_message, handle_next_word

TOKEN = "7049739914:AAH9tVuxZ_F4Pv5ahCmRx7yHW738IiuP1s8"


def start_polling():
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.reply_to(message, "Welcome! Let's start learning English words.")
        handle_next_word(message, bot)

    @bot.message_handler(commands=['next'])
    def handle_next(message):
        handle_next_word(message, bot)


    bot.polling(none_stop=True)


if __name__ == "__main__":
    start_polling()