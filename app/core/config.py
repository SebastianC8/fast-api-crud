class Settings():
    SECRET_KEY: str = "sebastian-corrales-clave-secreta-123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()