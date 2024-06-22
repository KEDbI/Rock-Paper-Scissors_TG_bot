from aiogram.types import Message
from aiogram import Router, F
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.filters import Command, CommandStart
from keyboards.keyboards import yes_no_kb, game_kb
from services.services import get_bot_choice, get_user_choice, get_winner
from database.database import update_column, get_stats, is_user_in_database, insert_new_user


router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message) -> None:
    check = is_user_in_database(user_id=message.from_user.id)
    if not check:
        insert_new_user(message.from_user.id)
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)


@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


@router.message(Command(commands='stats'))
async def process_stats_command(message: Message) -> None:
    stats = get_stats(message.from_user.id)
    if stats:
        await message.answer(text=f'{stats}', reply_markup=yes_no_kb)
    else:
        await message.answer(text=LEXICON_RU['no_stats'], reply_markup=yes_no_kb)


@router.message(F.text == LEXICON_RU['no_button'])
async def process_no_answer(message: Message) -> None:
    await message.answer(text=LEXICON_RU['no'])


@router.message(F.text == LEXICON_RU['yes_button'])
async def process_yes_button(message: Message) -> None:
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


@router.message(F.text.in_([LEXICON_RU['rock'],
                           LEXICON_RU['paper'],
                           LEXICON_RU['scissors']]))
async def process_game_button(message: Message) -> None:
    update_column(user_id=message.from_user.id, column_name='total_games',
                  value='total_games + 1')
    bot_choice = get_bot_choice()
    user_choice = get_user_choice(message.text)
    await message.answer(text=f'{LEXICON_RU['bot_choice']} - {LEXICON_RU[bot_choice]}')
    winner = get_winner(bot_choice, user_choice)
    if winner == 'user_won':
        update_column(user_id=message.from_user.id, column_name='won',
                      value='won + 1')
    await message.answer(text=f'{LEXICON_RU[winner]}', reply_markup=yes_no_kb)
