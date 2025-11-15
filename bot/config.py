from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("TG_SECRET_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")