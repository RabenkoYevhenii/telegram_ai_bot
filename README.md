# Telegram AI bot

## Project Overview:

* This bot helps users gather feedback on various locations in Kyiv by asking a series of questions.
* It uses OpenAI to generate insights based on the collected responses.
* The bot currently supports several locations:
    * Львівська площа
    * Бессарабський ринок
    * Алея Печерського парку
    * НСК Олімпійський
    * Київський Метрополітен

## Installation

1) Clone this repository:

```bash
git clone https://github.com/RabenkoYevhenii/telegram_ai_bot
```

2) Install the required libraries:

```bash
pip install -r requirements.txt
```

3) Create file .env and set variables as in .env_sample file .

## Running the Bot:

1) Start the bot:

```bash
python main.py
```

2) Open Telegram and add the bot as a contact using its [username](https://t.me/ai_analusis_bot).

3) Start a chat with the bot and follow the instructions.