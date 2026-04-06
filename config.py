from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SIMPLESWAP_API_KEY = os.getenv("SIMPLESWAP_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env файле")