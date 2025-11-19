import os
import threading
import time
import requests
from flask import Flask, jsonify
import bot

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "bot": "ULTRA BOMBER 3000+",
        "message": "Bot is active and running!"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

def run_bot():
    """Run the Telegram bot in a separate thread"""
    bot.main()

def self_ping():
    """Keep the server alive by pinging itself every 5 minutes"""
    time.sleep(30)  # Wait 30 seconds for server to start
    
    # Get Render URL from environment or construct it
    render_url = os.environ.get('RENDER_EXTERNAL_URL')
    
    if render_url:
        print(f"🌐 Self-ping enabled for: {render_url}")
        while True:
            try:
                response = requests.get(f"{render_url}/health", timeout=10)
                if response.status_code == 200:
                    print(f"✅ Self-ping successful - Bot is online!")
                else:
                    print(f"⚠️ Self-ping returned status: {response.status_code}")
            except Exception as e:
                print(f"❌ Self-ping failed: {e}")
            
            # Wait 5 minutes before next ping
            time.sleep(300)
    else:
        print("ℹ️ RENDER_EXTERNAL_URL not set - self-ping disabled")

if __name__ == '__main__':
    # Start the bot in a background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Start self-ping thread to keep bot alive (only on Render)
    if os.environ.get('RENDER_EXTERNAL_URL'):
        ping_thread = threading.Thread(target=self_ping, daemon=True)
        ping_thread.start()
    
    # Start the Flask web server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
