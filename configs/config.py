from os import environ

class Config:
    ENV = environ.get("CONTAINER_EXPORTER_ENV", "production")
    DEBUG = bool(int(environ.get("CONTAINER_EXPORTER_DEBUG", "0")))
    TESTING = DEBUG
    PORT = bool(int(environ.get("CONTAINER_EXPORTER_PORT", "8000")))