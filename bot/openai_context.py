from bot.questions import questions

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. "
        "User will send you data with answers "
        "on questions for specific location. "
        "Your task is to make a summary of "
        "this data in Ukrainian. "
        f"{questions}",
    }
]
