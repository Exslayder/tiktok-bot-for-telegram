import os
import tempfile
import shutil
import time
import yt_dlp
import telebot
from telebot import types
import traceback
import threading

API_TOKEN= TOKEN # Token from BotFather telegram
ALLOWED_USER_ID = YOUR_ID  # For personal use in restricted access
ACCESS_DENIED_MSG = "❌ Access denied. You are not authorized to use this bot."

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) # Directory for temporary files(In path of the script)
bot = telebot.TeleBot(API_TOKEN, parse_mode=None)

_temp_dirs: list[str] = []

shutdown_event = threading.Event()

def deny_access(chat_id):
    bot.send_message(chat_id, ACCESS_DENIED_MSG)

# Function for saving temporary files
def download_video_tempfile(url: str) -> tuple[str, str, str]:
    tmp_dir = tempfile.mkdtemp(prefix="tiktok_", dir=SCRIPT_DIR)
    _temp_dirs.append(tmp_dir)
    outtmpl = os.path.join(tmp_dir, 'video.%(ext)s')
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': outtmpl,
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'video')
        filename = ydl.prepare_filename(info)
        if not filename.lower().endswith('.mp4'):
            filename = os.path.splitext(filename)[0] + '.mp4'
    return filename, title, tmp_dir

# Command Start
@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    if message.from_user.id == ALLOWED_USER_ID:
        bot.send_message(message.chat.id, "👋 Hello, I'm Download-Bot for TikTok")
    else:
        deny_access(message.chat.id)

# Command stop
@bot.message_handler(commands=['stop'])
def handle_stop(message: types.Message):
    if message.from_user.id == ALLOWED_USER_ID:
        bot.send_message(message.chat.id, "🛑 The bot is finishing its work...")
        shutdown_event.set()
        bot.stop_polling()
    else:
        deny_access(message.chat.id)

# Other type content 
@bot.message_handler(content_types=["photo", "video", "audio", "document"])
def handle_others(message: types.Message):
    if message.from_user.id == ALLOWED_USER_ID:
        bot.send_message(
            message.chat.id,
            "Send me link on TikTok, please...",
            reply_to_message_id=message.message_id
        )
    else:
        deny_access(message.chat.id)

# Command text
@bot.message_handler(content_types=['text'])
def handle_text(message: types.Message):
    if message.from_user.id != ALLOWED_USER_ID:
        return deny_access(message.chat.id)
    url = message.text.strip()
    if 'tiktok.com' not in url:
        return bot.send_message(message.chat.id, "❗ Send me link on TikTok, please...")
    wait_msg = bot.send_message(message.chat.id, "⏬ Working...wait")
    video_path = title = tmp_dir = None
    try:
        video_path, title, tmp_dir = download_video_tempfile(url)
        with open(video_path, 'rb') as vid:
            bot.send_video(
                message.chat.id,
                vid,
                caption=f"✅ Say Thanks!\n{title}"
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠ Invalid URL. Try again please...: {e}")
    finally:
        if tmp_dir and os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
            _temp_dirs.remove(tmp_dir)
        try:
            bot.delete_message(message.chat.id, wait_msg.message_id)
        except:
            pass

def log_error(text: str):
    print(f"[ERROR NOTIFY] {text}")

def cleanup():
    print("[CLEANUP] We are starting a clean stop...")
    for d in list(_temp_dirs):
        if os.path.isdir(d):
            shutil.rmtree(d, ignore_errors=True)
            print(f"[CLEANUP] Temporary directory removed: {d}")
    _temp_dirs.clear()
    print("[CLEANUP] Completed.")

# Launch
if __name__ == '__main__':
    print("[INFO] Running a bot...")
    try:
        while not shutdown_event.is_set():
            try:
                bot.polling(timeout=60)
            except Exception:
                traceback.print_exc()
                log_error("The bot has crashed and will be restarted..")
                if shutdown_event.is_set():
                    break
                print("[INFO] Restart in 10 seconds...")
                time.sleep(10)
    finally:
        print("[INFO] Initiate cleanup before exiting.")
        cleanup()
        print("[INFO] Bot stopped.")