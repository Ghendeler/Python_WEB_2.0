from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    A class used to represent the application settings.

    Attributes
    ----------
    sqlalchemy_database_url : str
        The URL for the SQLAlchemy database.
    secret_key : str
        The secret key for the application.
    algorithm : str
        The algorithm used for encryption.
    mail_username : str
        The username for the mail server.
    mail_password : str
        The password for the mail server.
    mail_from : str
        The email address to send mail from.
    mail_port : int
        The port to use for the mail server.
    mail_server : str
        The server to use for sending mail.
    redis_host : str
        The host for the Redis server.
    redis_port : int
        The port for the Redis server.
    cloudinary_name : str
        The name of the Cloudinary account.
    cloudinary_api_key : str
        The API key for the Cloudinary account.
    cloudinary_api_secret : str
        The API secret for the Cloudinary account.
    """


    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str
    redis_port: int
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
