from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str

    @property
    def database_url(self):
        # postgresql+psycopg://DB_USER:DB_PASS@DB_HOST:DB_PORT/DB_NAME dsn connection
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_secret_key(self):
        return self.SECRET_KEY

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()