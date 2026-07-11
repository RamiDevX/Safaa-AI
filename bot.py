import os
import sys
import logging
import asyncio
import re
import shutil
from pathlib import Path
import uuid

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

import yt_dlp
from dotenv import load_dotenv

load_dotenv()

# --- Config ---

BOT_TOKEN = os.getenv("BOT_TOKEN")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "bot_data"
DATA_DIR.mkdir(exist_ok=True)

MAX_TELEGRAM_DOWNLOAD_MB = 20      
MAX_VIDEO_DURATION_SECONDS = 1800 


def safe_rmtree(path: Path, retries: int = 5, delay: float = 0.5):
    """Delete a directory, retrying on transient Windows file locks."""
    import time

    for attempt in range(retries):
        try:
            shutil.rmtree(path)
            return
        except PermissionError:
            if attempt == retries - 1:
                logger.warning(
                    f"Could not fully clean up {path} after {retries} attempts."
                )
                return
            time.sleep(delay)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(DATA_DIR / "bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("VocalRemoverBot")

YOUTUBE_REGEX = re.compile(
    r'(?:https?://)?(?:www\\.)?(?:youtube\\.com|youtu\\.be|youtube-nocookie\\.com)'
    r'/(?:watch\\?v=|embed/|v/|shorts/)?[a-zA-Z0-9_-]{11}\\S*'
)


class YouTubeService:
    @staticmethod
    async def download_audio(url: str, target_dir: Path) -> Path:
        def _sync_download():
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": str(target_dir / "input_track.%(ext)s"),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "socket_timeout": 30,
                "match_filter": yt_dlp.utils.match_filter_func(
                    f"duration < {MAX_VIDEO_DURATION_SECONDS}"
                ),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                return target_dir / "input_track.mp3"

        return await asyncio.to_thread(_sync_download)


class DemucsSeparatorService:
    def __init__(self, model_name: str = "htdemucs"):
        self.model_name = model_name

    async def separate_vocals(self, input_file_path: Path, output_base_dir: Path) -> Path:
        logger.info(f"Starting separation for: {input_file_path.name}")

        cmd = [
            "demucs",
            "--two-stems",
            "vocals",
            "-n",
            self.model_name,
            "-o",
            str(output_base_dir),
            str(input_file_path),
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        _, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode(errors="ignore")
            logger.error(f"Demucs failed: {error_msg}")
            raise RuntimeError("Vocal separation failed.")

        filename_stem = input_file_path.stem
        expected_vocal_path = (
            output_base_dir / self.model_name / filename_stem / "vocals.wav"
        )

        if not expected_vocal_path.exists():
            raise FileNotFoundError("Separated vocal file not found in output path.")

        return expected_vocal_path


router = Router()
separator_service = DemucsSeparatorService()


@router.message(Command("start"))
def cmd_start(message: Message):
    welcome_text = (
        "Welcome to the Vocal Remover Bot 🎤\n\n"
        "This bot separates the singer’s voice from the music using AI.\n\n"
        "📥 How to use:\n"
        "• Send a YouTube video link directly.\n"
        "• Or upload an audio file in MP3 format.\n\n"
        "⚙️ I’ll handle the rest and send you a clean audio track without music."
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Bot Developer",
                    url="https://t.me/ramidevx",
                )
            ]
        ]
    )

    return message.reply(welcome_text, reply_markup=keyboard)


async def process_audio_pipeline(
    message: Message,
    bot: Bot,
    source_type: str,
    source_data: str,
    file_ext: str = "mp3",
):
    request_id = str(uuid.uuid4())
    session_dir = DATA_DIR / request_id
    session_dir.mkdir(exist_ok=True)

    status_message = await message.reply("⏳ Request received, starting processing...")

    try:
        if source_type == "youtube":
            await status_message.edit_text("📥 Downloading audio from YouTube...")
            input_file = await YouTubeService.download_audio(source_data, session_dir)
        elif source_type == "file":
            await status_message.edit_text("📥 Downloading your audio file...")
            file_info = await bot.get_file(source_data)
            input_file = session_dir / f"input_track.{file_ext}"
            await bot.download_file(file_info.file_path, destination=input_file)
        else:
            raise ValueError("Unsupported source type.")

        await status_message.edit_text(
            "🤖 Separating vocals from music (this can take a minute)..."
        )
        vocals_wav = await separator_service.separate_vocals(input_file, session_dir)

        await status_message.edit_text("📤 Done! Sending your separated audio...")

        output_filename = f"Vocals_{message.from_user.id}_{request_id[:8]}.wav"
        vocal_audio_file = FSInputFile(path=vocals_wav, filename=output_filename)

        await message.reply_audio(
            audio=vocal_audio_file,
            caption="🎤 Vocals separated successfully. Enjoy!",
        )

        await status_message.delete()

    except Exception as e:
        logger.error(f"Error processing request {request_id}: {e}")
        await status_message.edit_text(
            "❌ Something went wrong while processing your file. "
            "Please check the file/link and try again."
        )

    finally:
        if session_dir.exists():
            safe_rmtree(session_dir)
            logger.info(f"Cleaned up session directory: {request_id}")


@router.message(F.text.regexp(YOUTUBE_REGEX))
async def handle_youtube_messages(message: Message, bot: Bot):
    match = YOUTUBE_REGEX.search(message.text)
    url = match.group(0) if match else message.text
    await process_audio_pipeline(message, bot, source_type="youtube", source_data=url)


@router.message(F.audio)
async def handle_audio_file_messages(message: Message, bot: Bot):
    file_size = message.audio.file_size or 0
    if file_size > MAX_TELEGRAM_DOWNLOAD_MB * 1024 * 1024:
        await message.reply(
            f"⚠️ File exceeds the {MAX_TELEGRAM_DOWNLOAD_MB}MB limit bots can download "
            "via the Telegram API. Please send a smaller file, or set up a local Bot API server."
        )
        return

    ext = "mp3"
    if message.audio.file_name and "." in message.audio.file_name:
        candidate = message.audio.file_name.rsplit(".", 1)[-1].lower()
        if re.fullmatch(r"[a-zA-Z0-9]{1,5}", candidate):
            ext = candidate

    await process_audio_pipeline(
        message,
        bot,
        source_type="file",
        source_data=message.audio.file_id,
        file_ext=ext,
    )


async def main():
    if not BOT_TOKEN:
        logger.critical("BOT_TOKEN environment variable is not set.")
        sys.exit(1)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Bot is running and polling for updates...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
