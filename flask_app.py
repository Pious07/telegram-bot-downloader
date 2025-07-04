from flask import Flask, request
import telegram
import os
from video_downloader import InstaVideoDownloader

app = Flask(__name__)


username = "clip_finder7"
password = "Clipper7784##"
print(f"🧪 IG_USER = {os.getenv('IG_USER')}")

BOT_TOKEN = '7290249545:AAFVUXcenil1Say82dveGmNo-egLiL8PLjE'
bot = telegram.Bot(token=BOT_TOKEN)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id")

    if message:
        reply = "📥 Starting downloads:\n\n"
        bot.send_message(chat_id=chat_id, text=reply)

        os.makedirs("Reels", exist_ok=True)

        downloader = InstaVideoDownloader()
        lines = message.strip().split("\n")

        for line in lines:
            try:
                rank, url, title = line.strip().split(",", 2)
                rank = int(rank.strip())
                title = title.strip()
                url = url.strip()

                filename = f"{rank} {title}"
                downloader.download(url, filename)
                reply += f"✅ {filename}.mp4 downloaded!\n"

            except Exception as e:
                reply += f"❌ Error processing line `{line}` — {e}\n"

        bot.send_message(chat_id=chat_id, text=reply)

    return "ok"
