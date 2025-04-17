from flask import Blueprint, render_template, request
from domain.repositories.genre_repository import GenreRepository

# Blueprint pour les routes liées aux séries TV
tv_bp = Blueprint('tv', __name__, url_prefix='/tv')

class TvController:
    """Contrôleur pour gérer les requêtes liées aux séries TV"""
    
    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository
        
        # Enregistrement des routes
        tv_bp.route('/')(self.index)
    
    def index(self):
        """Route principale pour les séries TV"""
        # Note: Cette méthode est un placeholder
        # Dans une implémentation complète, vous auriez des use cases
        # et repositories pour les séries TV
        genres = self.genre_repository.get_all()
        
        return render_template(
            'tv_shows.html',
            tv_shows=[],  # Liste vide pour l'instant
            genres=genres,
            title="Séries TV",
            active_page="tv"
        )
