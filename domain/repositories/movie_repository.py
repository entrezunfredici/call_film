from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.movie import Movie

class MovieRepository(ABC):
    """Interface pour l'accès aux données des films"""
    
    @abstractmethod
    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        """Récupère un film par son ID"""
        pass
    
    @abstractmethod
    def get_by_tmdb_id(self, tmdb_id: int) -> Optional[Movie]:
        """Récupère un film par son ID TMDB"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Movie]:
        """Récupère tous les films"""
        pass
    
    @abstractmethod
    def get_by_genre(self, genre_id: int) -> List[Movie]:
        """Récupère les films par genre"""
        pass
    
    @abstractmethod
    def search_by_title(self, title: str) -> List[Movie]:
        """Recherche des films par titre"""
        pass
    
    @abstractmethod
    def get_popular(self, limit: int = 20) -> List[Movie]:
        """Récupère les films populaires"""
        pass
    
    @abstractmethod
    def get_now_playing(self, limit: int = 20) -> List[Movie]:
        """Récupère les films actuellement en salle"""
        pass
    
    @abstractmethod
    def save(self, movie: Movie) -> Movie:
        """Sauvegarde un film"""
        pass
    
    @abstractmethod
    def delete(self, movie_id: int) -> bool:
        """Supprime un film par son ID"""
        pass
