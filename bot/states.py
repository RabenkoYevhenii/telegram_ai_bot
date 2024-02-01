from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionsForm(StatesGroup):
    location_name = State()
    first_question = State()
    second_question = State()
    third_question = State()
    fourth_question = State()
    fifth_question = State()
    comment_decision = State()
    comment = State()
    photo_decision = State()
    photo = State()
    save_data_to_db = State()
    send_info_to_openai = State()
    summary = State()
