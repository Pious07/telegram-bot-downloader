from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters
import os
from video_downloader import InstaVideoDownloader

app = Flask(__name__)

# ✅ Telegram Bot Setup
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telegram.Bot(token=BOT_TOKEN)

# ✅ Create Dispatcher for handling updates
dispatcher = Dispatcher(bot, None, use_context=True)

# ✅ Instagram Downloader
downloader = InstaVideoDownloader()

@app.route('/')
def home():
    return "✅ Telegram Bot Downloader is live and ready!"

# ✅ This is the endpoint Telegram will call (Webhook)
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

# ✅ Handle text messages (e.g., Instagram Reel links)
def handle_message(update, context):
    text = update.message.text
    chat_id = update.message.chat_id

    if "instagram.com" in text:
        update.message.reply_text("📥 Downloading your Instagram video...")
        try:
            downloader.download(text, "insta_video")
            output_file = "reels/insta_video.mp4"
            if os.path.exists(output_file):
                context.bot.send_video(chat_id=chat_id, video=open(output_file, 'rb'))
            else:
                context.bot.send_message(chat_id=chat_id, text="❌ Failed to find the downloaded video.")
        except Exception as e:
            context.bot.send_message(chat_id=chat_id, text=f"❌ Error: {str(e)}")
    else:
        context.bot.send_message(chat_id=chat_id, text="❓ Send me a valid Instagram Reel link.")

# ✅ Register the handler
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

if __name__ == "__main__":
    app.run(debug=True)
