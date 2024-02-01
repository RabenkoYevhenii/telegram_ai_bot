import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

storage = MemoryStorage()
bot = Bot(os.environ.get("BOT_TOKEN"))
dp = Dispatcher(bot=bot, storage=storage)


possible_answers = (
    "_Можливі відповіді: Так, Ні, або Коментар за допомогою "
    "вводу з клавіатури_"
)
