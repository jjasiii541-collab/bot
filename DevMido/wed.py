from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive and Running!"

@app.route('/health')
def health():
    return {"status": "ok"}, 200

def run():
    # Force binding to 0.0.0.0:5000 for Replit environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def start_flask():
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    print("Flask web server started on port 5000")
