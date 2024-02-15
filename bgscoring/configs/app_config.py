import os
from dotenv import load_dotenv

load_dotenv()

DB_ENGINE = os.environ.get("DB_ENGINE", "postgresql+asyncpg")
DB_NAME = os.environ.get("DB_NAME", "bgscoring")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "bgscoring")
DB_PASS = os.environ.get("DB_PASS", "bgscoring")

DB_NAME_TEST = os.environ.get("DB_NAME_TEST", "bgscoring_test")
DB_HOST_TEST = os.environ.get("DB_HOST_TEST", "db")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST", "5432")
DB_USER_TEST = os.environ.get("DB_USER_TEST", "bgscoring_test")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST", "bgscoring_test")

SECRET_AUTH: str = os.environ.get("SECRET_AUTH", "some-very-secret-auth-key")

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
