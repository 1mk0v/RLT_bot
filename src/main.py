import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from models import Request
from utils import Aggregator
from database.database import RLTDatabaseInterface


TOKEN = "your token"

dp = Dispatcher()
db = RLTDatabaseInterface()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message()
async def handlerOfAnythink(message: types.Message) -> None:
    try:
        request = Request(**eval(message.text))
        aggregator = Aggregator(await db.get(request), request)
        await message.answer(aggregator.aggregation())
    except Exception as error:
        print(error)
        await message.answer('Невалидный запрос. Пример запроса: \
                              {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
