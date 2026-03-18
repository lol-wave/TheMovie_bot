# 🎬 CineBot

A Telegram bot for storing and retrieving movies by code, with inline mode support and a full admin panel.

## ✨ Features

- **Get movies by code** — users enter a movie code to receive the video
- **Inline mode** — search movies by name directly from any chat
- **Admin panel** — add, delete, and edit movies with captions
- **Broadcast** — send messages or ads to all users with live progress tracking
- **Statistics** — view total users, movies added today/this week/this month

## 🚀 Usage

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/admin` | Open admin panel (admins only) |

**Inline mode:** Type `<movie_bot_username> <movie name>` in any chat to search and share a movie instantly.

## 🛠️ Tech Stack

- **Python**
- **aiogram 2.x** — Telegram bot framework
- **SQLite** — database for users and movies
- **FSM (Finite State Machine)** — multi-step admin flows
- **Inline mode** — movie search across any Telegram chat

## 📁 Project Structure

```
├── app.py                  # Entry point
├── loader.py               # Bot, dispatcher, db instances
├── handlers/
│   └── users/
│       └── movie_handler.py
├── keyboards/
│   ├── inline/
│   └── default/
├── states/
│   └── states.py
├── data/
│   └── config.py
└── utils/
    ├── notify_admins.py
    └── set_bot_commands.py
```

## ⚙️ Setup

1. Clone the repo
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file:
   ```
   BOT_TOKEN=your_bot_token_here
   ADMIN_ID=your_telegram_id_here
   ```
5. Run the bot:
   ```bash
   python app.py
   ```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

## 👤 Author

Made by [lol_wave](https://t.me/lol_wave)
