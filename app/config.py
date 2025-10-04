import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()  # Load variables from .env if present


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")


settings = Settings()


