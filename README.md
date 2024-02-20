## This project is a bot for Telegram that downloads videos from TikTok without a watermark
![](https://img.shields.io/badge/python3-black?link=https%3A%2F%2Fwww.python.org%2Fdownloads%2F)![](https://img.shields.io/badge/yt%20dlp-%238B0000?link=https%3A%2F%2Fpypi.org%2Fproject%2Fyt-dlp%2F)![](https://img.shields.io/badge/telebot-%230000CD?link=pip%20install%20pyTelegramBotAPI)

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

    3.1 Replace the word **TOKEN** with the token of your created bot:

    ```bash
    bot = telebot.TeleBot("TOKEN")
    ```

    3.2 Find out your ID using [**@userinfobot**](https://t.me/userinfobot) and replace the phrase **YOUR_ID**:

    ```bash
    allowed_user_id = YOUR_ID
    ```

    > [**@BotFather**](https://t.me/BotFather) and [**@userinfobot**](https://t.me/userinfobot) are the names of the bots in telegram.

    > **This ID** will help you to use the bot on your Telegram account only. This feature is available to prevent other users from using the bot.

    > How to create a bot and get **TOKEN**:

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
