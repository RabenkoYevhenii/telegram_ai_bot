from aiogram import types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from questions import questions

choose_location_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
choose_location_keyboard.add("Обрати локацію")

locations_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for location_name, _ in questions.items():
    locations_keyboard.add(KeyboardButton(text=location_name))


yesno_keyboard = types.ReplyKeyboardMarkup(row_width=2)
yesno_keyboard.add("Так").add("Ні")

next_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
next_keyboard.add("Далі")
