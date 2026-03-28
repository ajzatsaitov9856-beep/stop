import os
import json
import random
from datetime import datetime, timedelta, timezone

from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]
STRING_SESSION = os.environ["STRING_SESSION"]

def load_state():
    try:
        with open("state.json", "r") as f:
            return json.load(f)
    except:
        return {"next_send_at": None}

def save_state(state):
    with open("state.json", "w") as f:
        json.dump(state, f)

def load_messages():
    with open("messages.txt", "r", encoding="utf-8") as f:
        return [f.read()]

def load_targets():
    with open("targets.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def now():
    return datetime.now(timezone.utc)

def should_send(state):
    if not state["next_send_at"]:
        return True
    return now() >= datetime.fromisoformat(state["next_send_at"])

async def main():
    state = load_state()

    if not should_send(state):
        print("Еще рано")
        return

    messages = load_messages()
    targets = load_targets()

    message = random.choice(messages)
    target = random.choice(targets)

    client = TelegramClient(
        StringSession(STRING_SESSION),
        int(API_ID),
        API_HASH
    )

    async with client:
        await client.send_message(target, message)

    print("Отправлено")

    delay = random.randint(60, 120)
    next_time = now() + timedelta(minutes=delay)

    state["next_send_at"] = next_time.isoformat()
    save_state(state)

import asyncio
asyncio.run(main())
