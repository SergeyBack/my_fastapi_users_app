from pydantic import PostgresDsn
from pydantic import AmqpDsn
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
import logging

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

WORKER_LOG_DEFAULT_FORMAT = (
    # тут докидываем имя процесса - там будет имя и номер воркера
    "[%(asctime)s.%(msecs)03d] [%(processName)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

 
class GunicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    timeout: int = 800
    
    
class LoggingConfig(BaseModel):
    log_level: Literal[
        'debug',
        'info',
        'warning',
        'error',
        'crittical',
    ] = 'info'
    log_format: str = LOG_DEFAULT_FORMAT
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    
    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]
        

class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    messages: str = "/messages"
    service: str = "/service"
    
    
class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()
    
    @property
    def bearer_token_url(self)->str:
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path ="".join(parts)
        return path.removeprefix("/")


class TaskiqConfig(BaseModel):
    url: str ="amqp://guest:guest@rabbitmq:5672//" 
    log_format: str = WORKER_LOG_DEFAULT_FORMAT


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    
    naming_convention: dict[str,str] = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_N_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str
    

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("/home/sergo/projects/my_fastapi_app/fastapi-application/.env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )                   
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()
    taskiq: TaskiqConfig = TaskiqConfig()
    db: DatabaseConfig 
    access_token: AccessToken
    
    
settings =Settings()  # type: ignore

