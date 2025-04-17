from flask import Flask

def setup_dependencies(app: Flask) -> None:
    """
    Configure les dépendances de l'application et les injecte dans les contrôleurs
    
    Args:
        app: Instance de l'application Flask
    """
    # Repositories
    from domain.repositories.movie_repository import MovieRepository
    from domain.repositories.genre_repository import GenreRepository
    from infrastructure.repositories.sqlalchemy_movie_repository import SqlAlchemyMovieRepository
    from infrastructure.repositories.sqlalchemy_genre_repository import SqlAlchemyGenreRepository
    
    movie_repository: MovieRepository = SqlAlchemyMovieRepository()
    genre_repository: GenreRepository = SqlAlchemyGenreRepository()
    
    # Services externes
    from infrastructure.external_services.tmdb_api_service import TMDBApiService
    tmdb_service = TMDBApiService()
    
    # Use cases
    from domain.use_cases.get_popular_movies import GetPopularMoviesUseCase
    from domain.use_cases.search_movies import SearchMoviesUseCase
    from domain.use_cases.sync_movies import SyncMoviesUseCase
    
    get_popular_movies_use_case = GetPopularMoviesUseCase(movie_repository)
    search_movies_use_case = SearchMoviesUseCase(movie_repository)
    sync_movies_use_case = SyncMoviesUseCase(
        movie_repository,
        genre_repository,
        tmdb_service
    )
    
    # Stockage des instances pour accessibilité globale dans l'application
    app.config['REPOSITORIES'] = {
        'movie': movie_repository,
        'genre': genre_repository
    }
    
    app.config['SERVICES'] = {
        'tmdb': tmdb_service
    }
    
    app.config['USE_CASES'] = {
        'get_popular_movies': get_popular_movies_use_case,
        'search_movies': search_movies_use_case,
        'sync_movies': sync_movies_use_case
    }
    
    # Contrôleurs et routes
    from adapters.controllers.movie_controller import MovieController, movie_bp
    from adapters.controllers.tv_controller import TvController, tv_bp
    from adapters.controllers.tmdb_controller import TMDBController, tmdb_bp
    
    movie_controller = MovieController(
        get_popular_movies_use_case,
        search_movies_use_case,
        genre_repository
    )
    
    tv_controller = TvController(genre_repository)
    
    tmdb_controller = TMDBController(sync_movies_use_case)
    
    # Stockage des contrôleurs
    app.config['CONTROLLERS'] = {
        'movie': movie_controller,
        'tv': tv_controller,
        'tmdb': tmdb_controller
    }
    
    # Enregistrement des blueprints
    app.register_blueprint(movie_bp)
    app.register_blueprint(tv_bp)
    app.register_blueprint(tmdb_bp)
