from flask import Blueprint, jsonify
from domain.use_cases.sync_movies import SyncMoviesUseCase

# Blueprint pour les routes liées à la synchronisation TMDB
tmdb_bp = Blueprint('tmdb', __name__, url_prefix='/api/tmdb')

class TMDBController:
    """Contrôleur pour gérer les requêtes liées à l'API TMDB"""
    
    def __init__(self, sync_movies_use_case: SyncMoviesUseCase):
        self.sync_movies_use_case = sync_movies_use_case
        
        # Enregistrement des routes
        tmdb_bp.route('/sync', methods=['POST'])(self.sync)
    
    def sync(self):
        """Route pour déclencher une synchronisation manuelle avec TMDB"""
        result = self.sync_movies_use_case.execute()
        
        return jsonify({
            "success": True,
            "statistics": result
        })

    def get_now_playing_movies():
        response = requests.get(f"{TMDB_API_URL}/movie/now_playing", params={
            "api_key": TMDB_API_KEY,
            "language": "fr-FR",
            "page": 1
        })
        if response.status_code == 200:
            return response.json().get('results', [])
        return []