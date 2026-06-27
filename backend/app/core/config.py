from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings:
    PROJECT_NAME = "AI Stock Signal Pro"
    VERSION = "2.0.0"
    API_PREFIX = "/api"

    DEBUG = True


settings = Settings()