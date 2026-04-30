from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./ykzz_quant.db"
    JSL_COOKIE: str = ""
    TUSHARE_TOKEN: str = ""
    TUSHARE_RATE_LIMIT: int = 200  # calls per minute

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
