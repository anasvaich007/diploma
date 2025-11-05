import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.chitai-gorod.ru/"
API_BASE_URL = "https://web-agr.chitai-gorod.ru/web/api/v1/cart"
TOKEN = os.getenv("API_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}