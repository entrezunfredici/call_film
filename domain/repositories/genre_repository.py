from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.genre import Genre

class GenreRepository(ABC):
    """Interface pour l'accès aux données des genres"""
    
    @abstractmethod
    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        """Récupère un genre par son ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Genre]:
        """Récupère tous les genres"""
        pass
    
    @abstractmethod
    def save(self, genre: Genre) -> Genre:
        """Sauvegarde un genre"""
        pass
