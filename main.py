import asyncio
import logging
from aiogram import Dispatcher, Bot
from config_data.config import Config, load_config
from handlers import user_handlers, other_handlers
from aiogram.client.bot import DefaultBotProperties


# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(level='INFO',
                        format='#%(levelname)-8s [%(asctime)s] %(filename)s: %(lineno)d - %(name)s - %(message)s')
    logger.info('Starting bot')
    # Инициализируем конфиг
    config: Config = load_config()
    # Инициализируем бот и корневой роутер
    bot: Bot = Bot(token=config.tgbot.token,
                   default=DefaultBotProperties(parse_mode='HTML'))
    dp: Dispatcher = Dispatcher()

    #регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling1
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
