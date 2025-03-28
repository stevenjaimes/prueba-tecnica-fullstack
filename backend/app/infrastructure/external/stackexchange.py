import os
from dotenv import load_dotenv

load_dotenv()

class StackExchangeConfig:
    API_URL = os.getenv("STACKEXCHANGE_API_URL", "https://api.stackexchange.com/2.2/search")
    TIMEOUT = 10  # segundos