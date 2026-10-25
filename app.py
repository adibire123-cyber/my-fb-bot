from flask import Flask, request
import requests

app = Flask(__name__)

# আপনার ভেরিফিকেশন টোকেন
VERIFY_TOKEN = "nayem_bot_123" 

# আপনার পেজ অ্যাক্সেস টোকেন
PAGE_ACCESS_TOKEN = "EAAQl6JdiHZA8BS6Jd3jDG5JgFw5Nq3sTEboDzMwXmJZCySHzxPE0wPxsKZAl0pesw66CGzEjmX6rrKxM28YXzNgjte9aMDkdISplcwK6RXIVjz8p0a7XiM0N1ogkW1gF4ZBi1R7C5dFJUxozT35luZCGtiSBDax9clyKNZAqILgxsJ3xyeDZAKG4SoZCg7B0oK91I3wZAuQZDZD"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # ফেসবুক যখন ওয়েবহুক ভেরিফাই করবে
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        return "Verification failed", 403

    elif request.method == "POST":
        # কেউ মেসেজ পাঠালে এই অংশ কাজ করবে
        data = request.json
        if data.get("object") == "page":
            for entry in data.get("entry", []):
                for messaging in entry.get("messaging", []):
                    sender_id = messaging.get("sender", {}).get("id")
                    
                    if messaging.get("message") and not messaging["message"].get("is_echo"):
                        user_message = messaging["message"].get("text")
                        
                        # বটের উত্তর
                        ai_reply = f"ধন্যবাদ! আপনার বার্তাটি পেয়েছি: '{user_message}'"
                        
                        # ফেসবুক পেজে উত্তর পাঠিয়ে দেওয়া
                        send_message(sender_id, ai_reply)
                        
        return "EVENT_RECEIVED", 200

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(port=5000)