<div align="center">
  
#  Safaa-AI 🤖🎤

**Separate vocals from music using AI. Send a YouTube link or MP3.**

[![Telegram Bot](https://img.shields.io/badge/Telegram-@@SafaaVocals_bot-0088cc?style=flat-square&logo=telegram)](https://t.me/@SafaaVocals_bot)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

</div>

## Features

- 🎥 Extract audio directly from YouTube links
- 📤 Or upload an audio file straight from Telegram
- 🤖 AI-powered vocal isolation using [Demucs](https://github.com/facebookresearch/demucs) (`htdemucs` model)
- 🧹 Automatic cleanup of temporary files after each request
- ⚡ Fully async, handles multiple users concurrently

## Requirements

- Python 3.9+
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) installed and available on your system `PATH`
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/Safaa-AI.git
   cd Safaa-AI
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   ```

5. **Run the bot**
   ```bash
   python bot.py
   ```

## Usage

- `/start` — shows a welcome message and instructions
- Send a YouTube link — the bot downloads the audio and returns the isolated vocals
- Send/upload an audio file (up to 20 MB, the Telegram Bot API download limit) — same process

## Project Structure

```
Safaa-AI/
├── bot.py              # main bot logic
├── requirements.txt    # Python dependencies
├── .env                # bot token (not committed)
├── .gitignore
└── bot_data/            # runtime logs + temporary session files (auto-created)
```

## Notes

- The first run downloads the `htdemucs` model weights (~80 MB), so the first request will take longer than usual.
- Videos longer than 30 minutes are skipped to avoid excessive resource usage (configurable via `MAX_VIDEO_DURATION_SECONDS` in `bot.py`).
- Never commit your `.env` file or bot token to version control.

## Developer

**Rami Bitar**

[![Gmail](https://img.shields.io/badge/Gmail-000000?style=flat-square&logo=gmail&logoColor=EA4335)](mailto:ramibitar.connect@gmail.com)
[![Linktree](https://img.shields.io/badge/Linktree-000000?style=flat-square&logo=linktree&logoColor=43E55E)](https://linktr.ee/ramibitarr)
