import os
import tempfile
import shutil
import time
import yt_dlp
import telebot
from telebot import types

API_TOKEN= TOKEN # Token from BotFather telegram
ALLOWED_USER_ID = YOUR_ID  # For personal use in restricted access

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) # Directory for temporary files(In path of the script)
bot = telebot.TeleBot(API_TOKEN, parse_mode=None)

# Function for saving temporary files
def download_video_tempfile(url: str) -> tuple[str, str, str]:
    tmp_dir = tempfile.mkdtemp(prefix="tiktok_", dir=SCRIPT_DIR)
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
        bot.send_message(message.chat.id, "❌ Access denied. You are not authorized to use this bot.")

# Command stop
@bot.message_handler(commands=['stop'])
def handle_stop(message: types.Message):
    if message.from_user.id == ALLOWED_USER_ID:
        bot.send_message(message.chat.id, "🛑 Stop all...")
    else:
        bot.send_message(message.chat.id, "❌ Access denied. You are not authorized to use this bot.")

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
        bot.send_message(message.chat.id, "❌ Access denied. You are not authorized to use this bot.")

# Command text
@bot.message_handler(content_types=['text'])
def handle_text(message: types.Message):
    if message.from_user.id != ALLOWED_USER_ID:
        return bot.send_message(message.chat.id, "❌ Access denied. You are not authorized to use this bot.")
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
        try:
            bot.delete_message(message.chat.id, wait_msg.message_id)
        except:
            pass

# Launch
if __name__ == '__main__':
    import traceback
# Logging and raising the bot in case of failures
    def notify_owner(text):
        try:
            bot.send_message(ALLOWED_USER_ID, f"⚠️ {text}")
        except Exception as e:
            print("[ERROR] Failed to send notification to owner:", e)

    while True:
        try:
            print("[INFO] Start bot...")
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            error_text = traceback.format_exc()
            print("[ERROR] Failed:\n", error_text)
            notify_owner("The bot crashed with an error and will be restarted.")
            print("[INFO] Restart in 10 seconds...")
            time.sleep(10)
