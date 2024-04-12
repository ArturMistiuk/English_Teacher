import random
from api_client import get_random_word_and_definition


def send_new_word(user_id, bot):
    try:
        word, definition, pronunciation = get_random_word_and_definition()
    except ValueError:
        word = get_random_word_and_definition()
        definition = "Unknown"
        pronunciation = "Unknown"
    if word and definition and pronunciation:
        translation_text = f"Remember the word: {word}\n\nDefinition: {definition}\n\nPronunciation: {pronunciation}"  # Display only the first definition
        bot.send_message(user_id, translation_text)


def handle_next_word(message, bot):
    bot.send_message(message.chat.id, "Let's try the next word!")
    send_new_word(message.chat.id, bot)
