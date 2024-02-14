from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PYTHONPATH: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    MODE: str
    BOT_TOKEN: str
    ADMINT_CHAT: str
    SALE_GROUP: str

    @property
    def DB_URL(self):
        print(self.DB_NAME)
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')


settings = Settings()
# import os
# from dotenv import load_dotenv

# load_dotenv()

# BOT_TOKEN = os.environ.get("BOT_TOKEN")
# ADMINT_CHAT = os.environ.get("ADMINT_CHAT")
# SALE_GROUP = os.environ.get("SALE_GROUP")

# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# DB_NAME = os.environ.get("DB_NAME")
# DB_USER = os.environ.get("DB_USER")
# DB_PASS = os.environ.get("DB_PASS")
