#from pydantic_settings import BaseSettings
from pydantic import BaseSettings



class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str

    cloud_name: str
    api_key: str
    api_secret: str


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
