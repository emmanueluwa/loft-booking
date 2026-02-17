from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str
    telegram_chat_id: str
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
