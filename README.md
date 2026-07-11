<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=180&section=header&text=Safaa%20AI&fontSize=60&fontColor=fff&animation=fadeIn&fontAlignY=38&desc=Vocal%20Remover%20Bot&descAlignY=58&descAlign=50"/>

<p>
  <b>Separate vocals from music using AI. Send a YouTube link or an MP3 — get the vocals back, clean.</b>
</p>

<p>
  <a href="https://t.me/SafaaVocals_bot">
    <img src="https://img.shields.io/badge/Telegram-@SafaaVocals__bot-0088cc?style=for-the-badge&logo=telegram&logoColor=white" />
  </a>
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  </a>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

</div>

<br/>

## 📖 About

**Safaa AI** is a Telegram bot that isolates vocals from any song using AI. Drop a YouTube link or upload an MP3, and the bot handles the rest — no editing software, no manual work.

<br/>

## ✨ Features

| | |
|---|---|
| 🎥 | Extract audio directly from YouTube links |
| 📤 | Or upload an audio file straight from Telegram |
| 🤖 | AI-powered vocal isolation using [Demucs](https://github.com/facebookresearch/demucs) (`htdemucs` model) |
| 🧹 | Automatic cleanup of temporary files after every request |
| ⚡ | Fully async — handles multiple users concurrently |

<br/>

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-0088cc?style=for-the-badge&logo=telegram&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)
![Demucs](https://img.shields.io/badge/Demucs-black?style=for-the-badge&logo=meta&logoColor=white)
![yt--dlp](https://img.shields.io/badge/yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white)

</div>

<br/>

## 📋 Requirements

- Python 3.9+
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) installed and available on your system `PATH`
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

<br/>

## 🚀 Setup

**1. Clone the repo**
```bash
git clone https://github.com/<your-username>/Safaa-AI.git
cd Safaa-AI
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:
```env
BOT_TOKEN=your_telegram_bot_token_here
```

**5. Run the bot**
```bash
python bot.py
```

<br/>

## 💬 Usage

| Command / Action | Result |
|---|---|
| `/start` | Shows a welcome message and instructions |
| Send a YouTube link | Bot downloads the audio and returns the isolated vocals |
| Upload an audio file (≤ 20 MB) | Same process, straight from your file |

<br/>

## 📂 Project Structure

```
Safaa-AI/
├── bot.py              # Main bot logic
├── requirements.txt    # Python dependencies
├── .env                # Bot token (not committed)
├── .gitignore
└── bot_data/            # Runtime logs + temporary session files (auto-created)
```

<br/>

## 📝 Notes

> [!NOTE]
> The first run downloads the `htdemucs` model weights (~80 MB), so the first request takes longer than usual.

> [!NOTE]
> Videos longer than 30 minutes are skipped to avoid excessive resource usage — configurable via `MAX_VIDEO_DURATION_SECONDS` in `bot.py`.

> [!WARNING]
> Never commit your `.env` file or bot token to version control.

<br/>

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=gradient&height=3"/>

## 👨‍💻 Developer

<div align="center">

**Rami Bitar**

<a href="https://github.com/RamiDevX">
  <img src="https://img.shields.io/badge/GitHub-RamiDevX-161b22?style=for-the-badge&logo=github&logoColor=white" />
</a>
<a href="https://t.me/ramidevx">
  <img src="https://img.shields.io/badge/Telegram-@ramidevx-0088cc?style=for-the-badge&logo=telegram&logoColor=white" />
</a>
<a href="https://linkedin.com/in/rami-bitar-16479936b">
  <img src="https://img.shields.io/badge/LinkedIn-Rami%20Bitar-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>

<br/><br/>
<sub>Safaa AI © 2026</sub>

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer"/>
