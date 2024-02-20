## This project is a bot for Telegram that downloads videos from TikTok without a watermark

## How start

1.  Clone the repository:

    ```bash
    git clone https://github.com/Exslayder/tiktok-bot-for-telegram.git
    ```

2.  Install modules:

    ```bash
    pip install yt-dlp
    pip install pyTelegramBotAPI
    ```

3.  Create your bot using [**@BotFather**](https://t.me/BotFather) in telegram:

    3.1 Replace the word <span style='color:#BC8F8F'>**TOKEN**</span> with the token of your created bot:

    ```bash
    bot = telebot.TeleBot("TOKEN")
    ```

    3.2 Find out your ID using [**@userinfobot**](https://t.me/userinfobot) and replace the phrase <span style='color:red'>**YOUR_ID**</span>:

    ```bash
    allowed_user_id = YOUR_ID
    ```

    >[**@BotFather**](https://t.me/BotFather) and [**@userinfobot**](https://t.me/userinfobot) are the names of the bots in telegram.

    ><span style='color:red'>**This ID**</span> will help you to use the bot on your Telegram account only. This feature is available to prevent other users from using the bot.

    >How to create a bot and get <span style='color:#BC8F8F'>**TOKEN**</span>:

    ![How to create a bot and get TOKEN](https://assets-global.website-files.com/5d4bc52e7ec3666956bd3bf1/5ebd37e590f1424c4abfa1c2_botfather.jpg)

## Launch

1. Go to the project directory:

   ```bash
   cd tiktok-bot-for-telegram
   ```

2. Run the main script:

   ```bash
   python main.py
   ```

3. Send the video link to your bot and get the result.
