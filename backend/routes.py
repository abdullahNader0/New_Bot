from fastapi import APIRouter, Request
import os
import requests
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

@router.get("/webhook")
async def verify_webhook(request: Request):
    """ Facebook Messenger Webhook Verification """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return "Error: Invalid verification token"

@router.post("/webhook")
async def receive_message(request: Request):
    """ Handle incoming messages from Messenger """
    data = await request.json()

    if "entry" in data:
        for entry in data["entry"]:
            for messaging in entry.get("messaging", []):
                sender_id = messaging["sender"]["id"]
                if "message" in messaging:
                    message_text = messaging["message"]["text"]
                    send_message(sender_id, f"👋 مرحبًا! لقد قلت: {message_text}")

    return {"status": "ok"}

def send_message(recipient_id, text):
    """ Send message back to Facebook Messenger """
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
