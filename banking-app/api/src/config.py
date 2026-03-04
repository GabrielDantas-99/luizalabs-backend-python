from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore",
    env_file_encoding="utf-8"
  )
  
  environment: str = "production"
  
  database_url: str
  
  jwt_secret: str
  jwt_algorithm: str = "HS256"
  jwt_expire_minutes: int = 30
  
  allowed_origins: str = "*"
  
  @field_validator("jwt_secret")
  @classmethod
  def jwt_secret_must_be_strong(cls, value: str) -> str:
    if len(value) < 32:
      raise ValueError("JWT_SECRET deve ter pelo menos 32 caracteres.")
    return value
  
  @property
  def cors_origins(self) -> list[str]:
    return [o.strip() for o in self.allowed_origins.split(',')]
  
  @property
  def is_development(self) -> bool:
    return self.environment.lower() == "development"
  
settings = Settings()