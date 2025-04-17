import requests
from typing import List, Dict, Any, Optional
from config import get_config

class TMDBApiService:
    """Service pour interagir avec l'API TMDB"""
    
    def __init__(self):
        config = get_config()
        self.api_key = config.TMDB_API_KEY
        self.api_url = config.TMDB_API_URL
        self.poster_base_url = config.TMDB_POSTER_BASE_URL
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Effectue une requête à l'API TMDB
        
        Args:
            endpoint: Point d'entrée de l'API (sans la base URL)
            params: Paramètres de requête additionnels
            
        Returns:
            Données de réponse JSON ou dictionnaire vide en cas d'erreur
        """
        # Paramètres de base pour chaque requête
        request_params = {
            "api_key": self.api_key,
            "language": "fr-FR"
        }
        
        # Fusion avec les paramètres additionnels
        if params:
            request_params.update(params)
            
        # Exécution de la requête
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, params=request_params)
        
        if response.status_code == 200:
            return response.json()
        
        # Log de l'erreur (dans un vrai système on utiliserait un logger)
        print(f"Erreur API TMDB: {response.status_code} - {response.text}")
        return {}
    
    def fetch_genres(self) -> List[Dict[str, Any]]:
        """
        Récupère la liste des genres depuis l'API TMDB
        
        Returns:
            Liste des genres au format [{"id": 1, "name": "Action"}, ...]
        """
        response = self._make_request("/genre/movie/list")
        return response.get("genres", [])
    
    def fetch_popular_movies(self) -> List[Dict[str, Any]]:
        """
        Récupère les films populaires depuis l'API TMDB
        
        Returns:
            Liste des films populaires
        """
        response = self._make_request("/movie/popular", {"page": 1})
        return response.get("results", [])
    
    def fetch_now_playing_movies(self) -> List[Dict[str, Any]]:
        """
        Récupère les films actuellement en salle depuis l'API TMDB
        
        Returns:
            Liste des films en salle
        """
        response = self._make_request("/movie/now_playing", {"page": 1})
        return response.get("results", [])
    
    def search_movies(self, query: str) -> List[Dict[str, Any]]:
        """
        Recherche des films par nom
        
        Args:
            query: Terme de recherche
            
        Returns:
            Liste des films correspondant à la recherche
        """
        if not query:
            return []
            
        response = self._make_request("/search/movie", {
            "query": query,
            "page": 1
        })
        
        return response.get("results", [])
