from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "ContractClarify AI"
    environment: str = "development"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/contractclarify"

    class Config:
        env_file = ".env"

settings = Settings()