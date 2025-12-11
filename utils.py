import os
from config import config

def ensure_storage():
    if not os.path.exists(config.STORAGE_PATH):
        os.makedirs(config.STORAGE_PATH)
