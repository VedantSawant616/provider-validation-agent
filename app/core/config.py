from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int
    DATABASE_URL: str = ""  # Calculated below

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # APIs
    NPI_API_URL: str
    GOOGLE_MAPS_API_KEY: str
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Construct the database URL for SQLModel
        self.DATABASE_URL = f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

settings = Settings()