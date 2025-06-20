import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
raw_ids = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = set()
if raw_ids.strip():
    ADMIN_IDS = set(map(int, raw_ids.split(",")))
