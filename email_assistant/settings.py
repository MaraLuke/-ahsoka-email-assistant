from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    email_user: str = Field(..., env="EMAIL_USER")
    email_pass: str = Field(..., env="EMAIL_PASS")
    imap_server: str = "imap.seznam.cz"
    smtp_server: str = "smtp.seznam.cz"
    smtp_port: int = 465

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
