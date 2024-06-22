import random
from lexicon.lexicon_ru import LEXICON_RU


def get_bot_choice() -> str:
    return random.choice(['rock', 'paper', 'scissors'])


def get_user_choice(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            break
    return key


def get_winner(bot_choice: str, user_choice: str) -> str:
    rules = ['scissors>paper', 'rock>scissors', 'paper>rock']
    if bot_choice == user_choice:
        return 'draw'
    elif str(f'{bot_choice}>{user_choice}') in rules:
        return 'bot_won'
    else:
        return 'user_won'
