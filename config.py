import logging
import os

from utils import ensure_path

LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')

logging.basicConfig(level=logging.getLevelNamesMapping()[LOGGING_LEVEL])
logging.getLogger("httpx").setLevel(logging.WARNING)

TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN')

DATA_PATH = ensure_path(os.path.dirname(__file__), 'data')
PHOTO_PATH = ensure_path(DATA_PATH, 'photos')
AUDIO_PATH = ensure_path(DATA_PATH, 'audios')
