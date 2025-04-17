import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

class Config:
    """Configuration de base pour l'application"""
    SECRET_KEY = os.getenv("SECRET_KEY", "une_clé_par_défaut")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@db/{os.getenv('POSTGRES_DB')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration de l'API TMDB
    TMDB_API_KEY = os.getenv('API_KEY')
    TMDB_API_URL = "https://api.themoviedb.org/3"
    TMDB_POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
    
    # Configuration du planificateur
    SYNC_INTERVAL_MINUTES = int(os.getenv("SYNC_INTERVAL_MINUTES", 60))

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False

# Configuration à utiliser selon l'environnement
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retourne la configuration appropriée selon l'environnement"""
    env = os.getenv('FLASK_ENV', 'default')
    return config.get(env, config['default'])
