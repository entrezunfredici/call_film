from flask import Blueprint, render_template, request
from domain.use_cases.get_popular_movies import GetPopularMoviesUseCase
from domain.use_cases.search_movies import SearchMoviesUseCase
from domain.repositories.genre_repository import GenreRepository
from app.domain.tmdb_service import get_now_playing_movies

# Blueprint pour les routes liées aux films
movie_bp = Blueprint('movie', __name__, url_prefix='/movies')

class MovieController:
    """Contrôleur pour gérer les requêtes liées aux films"""
    
    def __init__(
        self, 
        get_popular_movies_use_case: GetPopularMoviesUseCase,
        search_movies_use_case: SearchMoviesUseCase,
        genre_repository: GenreRepository
    ):
        self.get_popular_movies_use_case = get_popular_movies_use_case
        self.search_movies_use_case = search_movies_use_case
        self.genre_repository = genre_repository
        
        # Enregistrement des routes
        movie_bp.route('/')(self.index)
        movie_bp.route('/popular')(self.popular)
        movie_bp.route('/now-playing')(self.now_playing)
        movie_bp.route('/search')(self.search)
    
    def index(self):
        """Route principale listant tous les films"""
        genre_id = request.args.get('genre', type=int)
        movies = self.get_popular_movies_use_case.execute(genre_id=genre_id)
        genres = self.genre_repository.get_all()
        
        return render_template(
            'movies.html',
            movies=movies,
            genres=genres,
            selected_genre=genre_id,
            title="Tous les films",
            active_page="movies"
        )
    
def popular(self):
    """Route pour les films populaires"""
    genre_id = request.args.get('genre', type=int)
    movies = self.get_popular_movies_use_case.execute(genre_id=genre_id)
    genres = self.genre_repository.get_all()
    
    return render_template(
        'movies.html',
        movies=movies,
        genres=genres,
        selected_genre=genre_id,
        title="Films populaires",
        active_page="popular"
    )

def now_playing(self):
    """Route pour les films actuellement en salle"""
    # On pourrait créer un use case spécifique pour les films en salle
    # Mais pour simplifier, on utilise le même que pour les films populaires
    # Un vrai système devrait avoir un use case dédié
    movies = self.get_popular_movies_use_case.execute()
    genres = self.genre_repository.get_all()
    
    return render_template(
        'movies.html',
        movies=movies,
        genres=genres,
        title="Films en salle",
        active_page="now_playing"
    )

def search(self):
    """Route pour la recherche de films"""
    query = request.args.get('q', '')
    genre_id = request.args.get('genre', type=int)
    
    movies = []
    if query:
        movies = self.search_movies_use_case.execute(query, genre_id)
        
    genres = self.genre_repository.get_all()
    
    return render_template(
        'search.html',
        movies=movies,
        query=query,
        genres=genres,
        selected_genre=genre_id,
        title=f"Recherche: {query}" if query else "Recherche",
        active_page="search"
    )