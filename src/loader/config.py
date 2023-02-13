from pydantic import BaseSettings

class Config(BaseSettings):
    host: str
    username: str
    port: int
    password: str
    database: str
    drivername: str

    class Config:
        case_sensitive: False
        env_prefix = 'DB_'