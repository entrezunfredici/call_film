from typing import List, Optional
from domain.entities.movie import Movie
from domain.repositories.movie_repository import MovieRepository

class GetPopularMoviesUseCase:
    """Cas d'utilisation pour récupérer les films populaires"""
    
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository
    
    def execute(self, genre_id: Optional[int] = None, limit: int = 20) -> List[Movie]:
        """
        Récupère les films populaires, éventuellement filtrés par genre
        
        Args:
            genre_id: Identifiant du genre pour filtrer (optionnel)
            limit: Nombre maximum de résultats
            
        Returns:
            Liste des films populaires
        """
        if genre_id:
            # Si un genre est spécifié, on récupère d'abord par genre
            movies = self.movie_repository.get_by_genre(genre_id)
            # Puis on trie par popularité (vote_average)
            movies.sort(key=lambda m: m.vote_average, reverse=True)
            return movies[:limit]
        else:
            # Sinon on récupère directement les films populaires
            return self.movie_repository.get_popular(limit)
