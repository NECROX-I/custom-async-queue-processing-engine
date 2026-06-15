from pydantic_settings import BaseSettings, SettingsConfigDict

#base settings class for the application
class Settings(BaseSettings):
    mode_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")    

#app
app_env: str = "development"
app_host: str = "0.0.0.0"
app_port: int = 8000
 
#database
database_url: str = ""

#redis
redis_url: str = ""

#queues
queue_high: str = "queue:high"
queue_normal: str = "queue:normal"
queue_low: str = "queue:low"
delayed_queue: str = "queue:delayed"

#worker
worker_name: str = "worker-1"
worker_concurrency: int = 4
job_timeout_seconds: int = 30
max_retries: int = 3
heartbeat_interval_seconds: int = 5
reaper_interval_seconds: int = 60
stuck_job_threshold_minutes: int = 5
scheduler_poll_seconds: int = 5
 
#property
@property
def is_development(self)-> bool:
    return self.app_env == "development"

@property
def priority_queues(self) -> list[str]:
    """High-Medium-Low for BRPOP priority"""
    return [self.queue_high, self.queue_normal, self.queue_low]

settings = Settings()