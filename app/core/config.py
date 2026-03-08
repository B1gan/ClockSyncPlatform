from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Clock Sync Platform"

    mysql_host: str = "127.0.0.1"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "root"
    mysql_db: str = "clock_sync"

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_db: int = 0

    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_topic_status: str = "device/status"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}?charset=utf8mb4"
        )


settings = Settings()

