import asyncio
import json
import os
import datetime
import config1
from telethon import TelegramClient, events
from telethon.tl.functions.messages import DeleteMessagesRequest

client = TelegramClient("session3", config1.api_id1, config1.api_hash1)
GROUPS_FILE = "group2.json"

def load_groups():
    if not os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "w") as f:
            json.dump([], f)
    with open(GROUPS_FILE, "r") as f:
        return json.load(f)

def save_groups(group_ids):
    with open(GROUPS_FILE, "w") as f:
        json.dump(group_ids, f)

def add_group(group_id):
    groups = load_groups()
    if group_id not in groups:
        groups.append(group_id)
        save_groups(groups)

def remove_group(group_id):
    groups = load_groups()
    if group_id in groups:
        groups.remove(group_id)
        save_groups(groups)

async def send_messages():
    group_ids = load_groups()
    for gid in group_ids:
        try:
            await client.send_message(gid, config1.text1)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] ✅ Yuborildi (text1): {gid}")
            await asyncio.sleep(60)
            await client.send_message(gid, config1.text2)
            now2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now2}] ✅ Yuborildi (text2): {gid}")
        except Exception as e:
            print(f"❌ Xatolik: {gid} — {e}")

@client.on(events.NewMessage(pattern=r"\.plus|\.delete|\.groups|\.status"))
async def command_handler(event):
    chat = await event.get_chat()
    group_id = chat.id
    text = event.raw_text.lower()

    if ".plus" in text:
        add_group(group_id)
        await event.respond("✅ Guruh ro‘yxatga qo‘shildi.")
    elif ".delete" in text:
        remove_group(group_id)
        await event.respond("❌ Guruh ro‘yxatdan o‘chirildi.")
    elif ".groups" in text:
        groups = load_groups()
        if not groups:
            await event.respond("📭 Guruhlar ro‘yxati bo‘sh.")
        else:
            msg = "📋 Yozilgan guruhlar:\n" + "\n".join([str(g) for g in groups])
            await event.respond(msg)
    elif ".status" in text:
        await event.respond("✅ Bot ishlayapti.")
    
    try:
        await client(DeleteMessagesRequest(group_id, [event.message.id]))
    except:
        pass

async def main():
    await client.start(config1.phone1)
    print("Bot ishga tushdi...")

    while True:
        await send_messages()
        await asyncio.sleep(config1.interval)

with client:
    client.loop.run_until_complete(main())
