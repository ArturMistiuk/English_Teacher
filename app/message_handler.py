import telebot
import random
from api_client import get_random_word_and_definition
from app.data import correct_answers, sentences

def handle_play(message, bot):
    # Select a random sentence and its correct answer
    idx = random.randint(0, len(sentences) - 1)
    sentence = sentences[idx]
    correct_answer = correct_answers[idx]

    # Include correct answer in choices if possible
    choices = [correct_answer]

    # Add random incorrect answers until we have 4 choices
    while len(choices) < 4:
        random_answer = random.choice(correct_answers)
        if random_answer not in choices:
            choices.append(random_answer)

    # Shuffle the choices to randomize their order
    random.shuffle(choices)

    # Send the fill-in-the-blank sentence with multiple choice options
    question_text = f"Complete the sentence:\n\n{sentence.replace('__________', '_____')}"
    options_text = "\n".join(f"{i+1}. {choice}" for i, choice in enumerate(choices))
    full_text = f"{question_text}\n\nOptions:\n{options_text}"

    # Store the correct answer for validation later
    bot.send_message(message.chat.id, full_text)

    # Define a callback to handle user responses
    def handle_answer(msg):
        try:
            answer_index = int(msg.text) - 1  # Convert user's choice to index
            if choices[answer_index] == correct_answer:
                bot.send_message(message.chat.id, "Correct!")
            else:
                bot.send_message(message.chat.id, "Incorrect.")

            # Ask if user wants to play again
            ask_play_again(message, bot)

        except (IndexError, ValueError):
            bot.send_message(message.chat.id, "Invalid choice. Please select a number from the options.")

    bot.register_next_step_handler(message, handle_answer)


def ask_play_again(message, bot):
    # Ask user if they want to play again
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('+', '-')

    msg = bot.send_message(message.chat.id, "Do you want to play again?", reply_markup=keyboard)

    # Define a callback to handle user response to play again
    def handle_play_again_response(msg):
        if msg.text == '+':
            handle_play(message, bot)  # Start a new game
        elif msg.text == '-':
            bot.send_message(message.chat.id, "Goodbye! Have a nice day.")  # Say goodbye
        else:
            bot.send_message(message.chat.id, "Invalid choice. Please use the provided buttons.")
            ask_play_again(message, bot)  # Ask again if invalid choice

    bot.register_next_step_handler(msg, handle_play_again_response)


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