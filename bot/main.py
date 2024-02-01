import os

import openai
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageTextIsEmpty
from sqlalchemy.orm import Session

from bot.openai_context import messages
from config import dp, possible_answers, bot
from db.engine import engine
from db.models import User, UserResponse, Base
from keyboards import (
    locations_keyboard,
    yesno_keyboard,
    choose_location_keyboard,
    next_keyboard,
)
from questions import questions
from states import QuestionsForm

Base.metadata.create_all(engine)


@dp.message_handler(text="/start")
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привіт, {message.from_user.first_name}! Почнімо працювати.",
        reply_markup=choose_location_keyboard,
    )


@dp.message_handler(text="/finish")
async def finish_handler(message: types.Message, state: FSMContext):

    await state.finish()

    await message.answer(
        "Ви зупинили роботу з ботом, щоб почати знову, використайте /start"
    )


@dp.message_handler(text="Обрати локацію")
async def cmd_choose_location(message: types.Message):
    await message.answer(
        "Оберіть будь яку локацію для заповнення чек листа",
        reply_markup=locations_keyboard,
    )


@dp.message_handler()
async def handle_message(message: types.Message, state: FSMContext):
    location_name = message.text
    await QuestionsForm.location_name.set()
    async with state.proxy() as data:
        data["location_name"] = location_name
    await bot.send_message(
        chat_id=message.from_user.id,
        text=questions[location_name][0] + "\n" + possible_answers,
        reply_markup=yesno_keyboard,
        parse_mode="Markdown",
    )

    await QuestionsForm.next()


@dp.message_handler(state=QuestionsForm.first_question)
async def answer_question1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        location_name = data.get("location_name")
        data["question1"] = message.text
    await message.answer(
        text=questions[location_name][1] + "\n" + possible_answers,
        reply_markup=yesno_keyboard,
        parse_mode="Markdown",
    )
    await QuestionsForm.next()


@dp.message_handler(state=QuestionsForm.second_question)
async def answer_question2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        location_name = data.get("location_name")
        data["question2"] = message.text
    await message.answer(
        text=questions[location_name][2] + "\n" + possible_answers,
        reply_markup=yesno_keyboard,
        parse_mode="Markdown",
    )
    await QuestionsForm.next()


@dp.message_handler(state=QuestionsForm.third_question)
async def answer_question3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        location_name = data.get("location_name")
        data["question3"] = message.text
    await message.answer(
        text=questions[location_name][3] + "\n" + possible_answers,
        reply_markup=yesno_keyboard,
        parse_mode="Markdown",
    )
    await QuestionsForm.next()


@dp.message_handler(state=QuestionsForm.fourth_question)
async def answer_question4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        location_name = data.get("location_name")
        data["question4"] = message.text
    await message.answer(
        text=questions[location_name][4] + "\n" + possible_answers,
        reply_markup=yesno_keyboard,
        parse_mode="Markdown",
    )
    await QuestionsForm.next()


@dp.message_handler(state=QuestionsForm.fifth_question)
async def answer_question5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["question5"] = message.text
    await message.answer(
        "Бажаєте залишити коментар?", reply_markup=yesno_keyboard
    )
    await QuestionsForm.next()


@dp.message_handler(state=QuestionsForm.comment_decision)
async def comment_decision(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["comment_decision"] = message.text
    if message.text == "Так":
        await message.answer("Можете написати ваш коментар нижче")
        await QuestionsForm.next()
    elif message.text == "Ні":
        await message.answer("Дякуємо за ваш відгук!")
        await message.answer("Секунду, зберігаю інформацію")
        await QuestionsForm.save_data_to_db.set()


@dp.message_handler(state=QuestionsForm.comment)
async def comment_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["comment"] = message.text
    await message.answer(
        "Дякуємо за додатковий коментар. Можливо бажаєте прикріпити фото?",
        reply_markup=yesno_keyboard,
    )
    await QuestionsForm.next()


@dp.message_handler(state=QuestionsForm.photo_decision)
async def photo_decision(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo_decision"] = message.text
    if message.text == "Так":
        await QuestionsForm.next()
        await message.reply(
            "Надішліть 1 фотографію з вашого візиту",
        )
    elif message.text == "Ні":
        await message.answer("Дякуємо за ваш відгук!")
        await message.answer(
            "Секунду, зберігаю інформацію", reply_markup=next_keyboard
        )
        await QuestionsForm.save_data_to_db.set()


@dp.message_handler(
    state=QuestionsForm.photo, content_types=types.ContentType.PHOTO
)
async def photo_handler(message: types.Message, state: FSMContext):
    photo = message.photo[-1]

    photo_file_id = photo.file_id

    async with state.proxy() as data:
        data["photo_file_id"] = photo_file_id

    await message.answer("Фотографія прийнята.")
    await message.answer("Дякуємо за ваш відгук!")
    await message.answer(
        "Секунду, зберігаю інформацію", reply_markup=next_keyboard
    )
    await QuestionsForm.next()


@dp.message_handler(state=QuestionsForm.save_data_to_db)
async def save_data_to_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        with Session(engine) as session:
            user = User(
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )
            session.add(user)
            session.commit()
            user_id = user.id

            user_response = UserResponse(
                user_id=user_id,
                location_name=data.get("location_name"),
                question1=data.get("question1", ""),
                question2=data.get("question2", ""),
                question3=data.get("question3", ""),
                question4=data.get("question4", ""),
                question5=data["question5"],
                comment=data.get("comment", ""),
                photo_id=data.get("photo_file_id", ""),
            )
            session.add(user_response)
            session.commit()
    await QuestionsForm.next()
    await message.answer("Інформація збережена", reply_markup=next_keyboard)


@dp.message_handler(state=QuestionsForm.send_info_to_openai)
async def send_info_to_openai(message: types.Message, state: FSMContext):
    await message.answer("Формується звіт від OpenAI...")
    await get_chat_gpt(message, state)


async def get_chat_gpt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_text = {
            "location_name": data.get("location_name"),
            "question1": data.get("question1"),
            "question2": data.get("question2"),
            "question3": data.get("question3"),
            "question4": data.get("question4"),
            "question5": data.get("question5"),
            "comment": data.get("comment", ""),
        }
    try:
        msg_for_user = await openai_message(
            message=message, msg_for_openai=user_text
        )
        await message.answer(text=msg_for_user)
    except MessageTextIsEmpty:
        pass


async def openai_message(message: types.Message, msg_for_openai: dict):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = "gpt-3.5-turbo"
    messages.append({"role": "user", "content": msg_for_openai})
    try:
        response = openai.ChatCompletion.create(model=model, messages=messages)
        return response.choices[0].message.content
    except openai.error.RateLimitError:
        await message.answer(
            "На даний момент OpenAI API недоступна для"
            " безкоштовного використання",
            reply_markup=next_keyboard,
        )
    await QuestionsForm.summary.set()


@dp.message_handler(state=QuestionsForm.summary)
async def summary_handler(message: types.Message, state: FSMContext):
    await message.answer("Дякуємо за відгук!")
    await state.finish()
    await message.answer("Секунду, переходимо в головне меню")
    await cmd_choose_location(message)


@dp.message_handler()
async def unknown_command(message: types.Message):
    await message.reply(
        "Вибач, я не розумію дану команду. Використовуй вбудований "
        "функціонал для коректної взаємодії з ботом"
    )


if __name__ == "__main__":
    executor.start_polling(dp)
