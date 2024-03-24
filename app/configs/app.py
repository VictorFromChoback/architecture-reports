from pydantic import BaseModel
from pydantic_settings import BaseSettings


class AppConfig(BaseModel):
    port: int
    host: str


class PostgresConfig(BaseModel):
    user: str
    password: str
    db: str
    port: int = 5432


class TokenConfig(BaseModel):
    jwt_algo: str
    secret: str


class Settings(BaseSettings):
    app: AppConfig
    postgres: PostgresConfig
    token: TokenConfig

    class Config:
        case_sensitive = False
        env_nested_delimiter = "__"


app_settings = Settings()
