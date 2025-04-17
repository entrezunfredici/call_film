from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Instance SQLAlchemy globale
db = SQLAlchemy()

def init_db(app: Flask) -> None:
    """
    Initialise la base de données avec l'application Flask
    
    Args:
        app: Instance de l'application Flask
    """
    db.init_app(app)
    
    with app.app_context():
        # Import ici pour éviter les imports circulaires
        from infrastructure.db.models import movie_model, genre_model
        
        # Création des tables
        db.create_all()