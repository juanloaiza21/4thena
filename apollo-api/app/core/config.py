from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    TWILIO_API_KEY: str
    TWILIO_API_SECRET: str
    TWILIO_APP_SID: str
    NGROK_URL: str | None = None
    MEETING_BAAS_API_KEY: str | None = None
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
