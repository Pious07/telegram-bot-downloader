from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Downloader Bot is live!"

# Include the rest of your bot logic below...
