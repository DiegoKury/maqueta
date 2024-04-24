import os

class Settings:
    database_name: str = os.getenv('DB_NAME', 'mydatabase')
    database_user: str = os.getenv('DB_USER', 'myuser')
    database_password: str = os.getenv('DB_PASSWORD', 'mypassword')
    database_host: str = os.getenv('DB_HOST', 'localhost')
    database_port: str = os.getenv('DB_PORT', '5432')

settings = Settings()
