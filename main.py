import yt_dlp
import telebot
import time


bot = telebot.TeleBot("TOKEN") # Token from BotFather telegram

allowed_user_id = YOUR_ID  # For personal use in restricted access

# Command Start


@bot.message_handler(commands=['start'])
def c_start(message):
    if message.from_user.id == allowed_user_id:
        bot.send_message(
            message.chat.id, "Hello, I'm Download-Bot for TikTok"
        )
        time.sleep(2)
        bot.send_message(
            message.chat.id, "Send me link on TikTok, please...")
    else:
        bot.send_message(
            message.chat.id, "Access denied. You are not authorized to use this bot.")

# Command stop


@bot.message_handler(commands=['stop'])
def c_stop(message):
    message_text = message.text.lower()
    if 'stop' in message_text:
        bot.send_message(message.chat.id, "Stop all...")

# Other type content !!! Will do something !!!


@bot.message_handler(content_types=["document", "photo", "video", "audio"])
def c_others(message):
    if message.from_user.id == allowed_user_id:
        bot.send_message(message.chat.id, "Send me link on TikTok, please...",
                         reply_to_message_id=message.message_id)
    else:
        bot.send_message(
            message.chat.id, "Access denied. You are not authorized to use this bot.")

# Command text


@bot.message_handler(content_types=['text'])
def c_text(message):
    if message.from_user.id == allowed_user_id:
        message_text = message.text.lower()
        if 'tiktok' in message_text:
            ytdlp_tiktok(message)
        else:
            bot.send_message(
                message.chat.id, "Sorry. I can only dowload video from TikTok")
    else:
        bot.send_message(
            message.chat.id, "Access denied. You are not authorized to use this bot.")

# yt_dlp


def ytdlp_tiktok(message):
    message_text = message.text.lower()
    if 'stop' in message_text:
        bot.send_message(message.chat.id, "Stop...")
    else:
        try:
            rab = bot.send_message(message.chat.id, "Working...wait")
            mobile_url = message.text
            ydl_opts = {
                'format': 'bv*+ba/b',
                'merge_output_format': 'mp4'
            }
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            info = ydl.extract_info(mobile_url, download=False)
            video_download_url = info['url']
            while True:
                bot.delete_message(message.chat.id, rab.message_id)
                bot.send_document(message.chat.id, document=video_download_url,
                                  caption=mobile_url + '\n Say Thanks! 🔥🔥🔥')
                break
        except Exception:
            bot.delete_message(message.chat.id, rab.message_id)
            send = bot.send_message(
                message.chat.id, "Invalid URL. Try again please...")
            bot.register_next_step_handler(send, ytdlp_tiktok)


max_attempts = 2
current_attempt = 0

# Block for handling errors associated with continuous use


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        current_attempt += 1
        print(f"An error has occurred: {str(e)}")
        if current_attempt >= max_attempts:
            print("The maximum number of attempts has been reached. Stopping the application.")
            break
        else:
            print(
                f"Trying to get the update again. Attempt №{current_attempt}")
            time.sleep(10)  # Pause before trying again