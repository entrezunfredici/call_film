import json
import os
from datetime import datetime, timedelta

CACHE_DIR = "cache"

def save_to_cache(filename, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(os.path.join(CACHE_DIR, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_cache(filename, max_age_minutes=60):
    path = os.path.join(CACHE_DIR, filename)
    if not os.path.exists(path):
        return None
    # Vérifie l'âge du fichier
    if datetime.now() - datetime.fromtimestamp(os.path.getmtime(path)) > timedelta(minutes=max_age_minutes):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
