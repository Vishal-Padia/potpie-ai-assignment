import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
