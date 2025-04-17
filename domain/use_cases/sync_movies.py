from typing import Dict, List, Any
from domain.entities.movie import Movie
from domain.entities.genre import Genre
from domain.repositories.movie_repository import MovieRepository
from domain.repositories.genre_repository import GenreRepository

class SyncMoviesUseCase:
    """Cas d'utilisation pour synchroniser les films depuis une source externe"""
    
    def __init__(
        self, 
        movie_repository: MovieRepository, 
        genre_repository: GenreRepository, 
        tmdb_service: Any  # Type Any pour éviter la dépendance cyclique
    ):
        self.movie_repository = movie_repository
        self.genre_repository = genre_repository
        self.tmdb_service = tmdb_service
    
    def execute(self) -> Dict[str, int]:
        """
        Synchronise les films et genres depuis l'API TMDB
        
        Returns:
            Dictionnaire contenant les statistiques de synchronisation
        """
        # Synchroniser les genres d'abord
        tmdb_genres = self.tmdb_service.fetch_genres()
        genres_count = 0
        
        for genre_data in tmdb_genres:
            genre = Genre(id=genre_data["id"], name=genre_data["name"])
            self.genre_repository.save(genre)
            genres_count += 1
        
        # Récupérer les films populaires et en salle
        tmdb_movies = self.tmdb_service.fetch_popular_movies()
        tmdb_movies.extend(self.tmdb_service.fetch_now_playing_movies())
        
        # Dédoublonnage par ID TMDB
        unique_movies = {movie["id"]: movie for movie in tmdb_movies}.values()
        movies_count = 0
        
        for movie_data in unique_movies:
            # Conversion des données TMDB en entité de domaine
            movie = Movie(
                tmdb_id=movie_data["id"],
                title=movie_data["title"],
                overview=movie_data["overview"],
                release_date=movie_data.get("release_date", ""),
                vote_average=movie_data.get("vote_average", 0.0),
                poster_path=movie_data.get("poster_path", ""),
                genre_ids=movie_data.get("genre_ids", [])
            )
            
            # Sauvegarde dans le repository
            self.movie_repository.save(movie)
            movies_count += 1
        
        return {
            "genres_synced": genres_count,
            "movies_synced": movies_count
        }
