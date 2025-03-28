# app/infrastructure/security/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class SecurityConfig:
    SECRET_KEY = os.getenv('SECRET_KEY') 