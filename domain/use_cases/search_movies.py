from typing import List, Optional
from domain.entities.movie import Movie
from domain.repositories.movie_repository import MovieRepository

class SearchMoviesUseCase:
    """Cas d'utilisation pour rechercher des films"""
    
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository
    
    def execute(self, query: str, genre_id: Optional[int] = None) -> List[Movie]:
        """
        Recherche des films par titre, éventuellement filtrés par genre
        
        Args:
            query: Terme de recherche
            genre_id: Identifiant du genre pour filtrer (optionnel)
            
        Returns:
            Liste des films correspondant à la recherche
        """
        # Si la requête est vide, on retourne une liste vide
        if not query:
            return []
            
        # Recherche par titre
        movies = self.movie_repository.search_by_title(query)
        
        # Filtre par genre si spécifié
        if genre_id:
            movies = [movie for movie in movies if genre_id in movie.genre_ids]
            
        return movies
