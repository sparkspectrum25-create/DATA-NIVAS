import os


class Settings:
    # Required. If unset, every protected route returns 503 (fail closed).
    token: str = os.environ.get("FRIDAY_TOKEN", "")


settings = Settings()
