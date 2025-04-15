#mvc avec stockage (pas fini)
from flask import Flask
from app.models import db
from app.domain.tmdb_service import tmdb_bp
from cron.scheduler import create_scheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(tmdb_bp)

create_scheduler(app)

@app.before_first_request
def create_tables():
    db.create_all()

# ancienne architecture (bordélique mais ok)
# app.py
# from flask import Flask, render_template, request, redirect, url_for
# import requests
# import os
# from dotenv import load_dotenv

# # Chargement des variables d'environnement
# load_dotenv()

# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'une_clé_secrète_par_défaut')

# db_user = os.getenv("POSTGRES_USER")
# db_password = os.getenv("POSTGRES_PASSWORD")
# db_name = os.getenv("POSTGRES_DB")
# db_host = "db"  # nom du service Docker

# # Configuration de l'API TMDB
# TMDB_API_KEY = os.getenv('API_KEY')
# TMDB_API_URL = "https://api.themoviedb.org/3"
# POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

# def get_now_playing_movies():
#     """Récupère les films actuellement en salle"""
#     endpoint = f"{TMDB_API_URL}/movie/now_playing"
#     params = {
#         "api_key": TMDB_API_KEY,
#         "language": "fr-FR",
#         "page": 1
#     }
    
#     response = requests.get(endpoint, params=params)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"results": []}

# def get_popular_movies():
#     """Récupère les films les plus populaires"""
#     endpoint = f"{TMDB_API_URL}/movie/popular"
#     params = {
#         "api_key": TMDB_API_KEY,
#         "language": "fr-FR",
#         "page": 1
#     }
    
#     response = requests.get(endpoint, params=params)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"results": []}

# def search_movies(query):
#     """Recherche des films par nom"""
#     endpoint = f"{TMDB_API_URL}/search/movie"
#     params = {
#         "api_key": TMDB_API_KEY,
#         "language": "fr-FR",
#         "query": query,
#         "page": 1
#     }
    
#     response = requests.get(endpoint, params=params)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"results": []}

# def get_movie_genres():
#     """Récupère la liste des genres de films"""
#     endpoint = f"{TMDB_API_URL}/genre/movie/list"
#     params = {
#         "api_key": TMDB_API_KEY,
#         "language": "fr-FR"
#     }
    
#     response = requests.get(endpoint, params=params)
    
#     if response.status_code == 200:
#         return response.json()["genres"]
#     else:
#         return []

# def get_top_rated_tv_shows():
#     """
#     Récupère les séries TV les mieux notées depuis l'API TMDB
#     """
#     endpoint = f"{TMDB_API_URL}/tv/popular"
#     params = {
#         "api_key": TMDB_API_KEY,
#         "language": "fr-FR"
#     }
#     params = {
#         "api_key": TMDB_API_KEY,
#         "language": "fr-FR",
#         "page": 1
#     }
    
#     response = requests.get(endpoint, params=params)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"results": []}

# def get_tv_genres():
#     """
#     Récupère les genres de séries TV depuis l'API TMDB
#     """
#     endpoint = f"{TMDB_API_URL}/genre/tv/list"
#     params = {
#         "api_key": os.environ.get("TMDB_API_KEY"),
#         "language": "fr-FR"
#     }
#     response = requests.get(endpoint, params=params)
    
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"results": []}

# def format_movies(movies):
#     """Formate les données des films pour l'affichage"""
#     for movie in movies:
#         if movie.get("poster_path"):
#             movie["poster_url"] = f"{POSTER_BASE_URL}{movie['poster_path']}"
#         else:
#             movie["poster_url"] = "/static/no-poster.jpg"
#     return movies

# def format_tv_shows(tv_shows):
#     """
#     Formate les données des séries TV pour l'affichage
#     """
#     for show in tv_shows:
#         # Gérer le cas où il n'y a pas d'image
#         if show.get('poster_path'):
#             show['poster_url'] = f"{POSTER_BASE_URL}{show['poster_path']}"
#         else:
#             show['poster_url'] = url_for('/static/no-poster.jpg')
        
#         # Remplacer le champ 'title' par 'name' pour les séries TV
#         if 'name' in show and 'title' not in show:
#             show['title'] = show['name']
            
#         # Gérer le champ 'first_air_date' au lieu de 'release_date'
#         if 'first_air_date' in show and 'release_date' not in show:
#             show['release_date'] = show['first_air_date']
    
#     return tv_shows

# @app.route('/')
# def home():
#     """Page d'accueil avec les boutons de navigation"""
#     return render_template('home.html')

# @app.route('/now-playing')
# def now_playing():
#     """Page des films en salle"""
#     # Récupération des films en salle
#     now_playing = get_now_playing_movies()
#     movies = now_playing.get("results", [])
    
#     # Récupération des genres
#     genres = get_movie_genres()
    
#     # Création d'un dictionnaire pour faciliter l'accès aux noms des genres
#     genre_dict = {genre["id"]: genre["name"] for genre in genres}
    
#     # Filtre par genre si spécifié
#     genre_id = request.args.get('genre', type=int)
#     if genre_id:
#         movies = [movie for movie in movies if genre_id in movie.get("genre_ids", [])]
    
#     # Ajout de l'URL complète des posters
#     movies = format_movies(movies)
    
#     return render_template('movies.html', 
#                           movies=movies, 
#                           genres=genres, 
#                           selected_genre=genre_id, 
#                           title="Films actuellement au cinéma",
#                           active_page="now-playing")

# @app.route('/popular')
# def popular():
#     """Page des films populaires"""
#     # Récupération des films populaires
#     popular_data = get_popular_movies()
#     movies = popular_data.get("results", [])
    
#     # Récupération des genres
#     genres = get_movie_genres()
    
#     # Filtre par genre si spécifié
#     genre_id = request.args.get('genre', type=int)
#     if genre_id:
#         movies = [movie for movie in movies if genre_id in movie.get("genre_ids", [])]
    
#     # Ajout de l'URL complète des posters
#     movies = format_movies(movies)
    
#     return render_template('movies.html', 
#                           movies=movies, 
#                           genres=genres, 
#                           selected_genre=genre_id, 
#                           title="Films populaires",
#                           active_page="popular")

# @app.route('/search')
# def search():
#     """Page de recherche de films"""
#     query = request.args.get('query', '')
    
#     if not query:
#         return render_template('search.html', movies=[], query='')
    
#     # Recherche des films
#     search_results = search_movies(query)
#     movies = search_results.get("results", [])
    
#     # Récupération des genres
#     genres = get_movie_genres()
    
#     # Filtre par genre si spécifié
#     genre_id = request.args.get('genre', type=int)
#     if genre_id:
#         movies = [movie for movie in movies if genre_id in movie.get("genre_ids", [])]
    
#     # Ajout de l'URL complète des posters
#     movies = format_movies(movies)
    
#     return render_template('search.html', 
#                           movies=movies, 
#                           genres=genres, 
#                           selected_genre=genre_id, 
#                           query=query,
#                           active_page="search")

# # Remplacez la route '/popular' par '/top-rated-tv'
# @app.route('/top-rated-tv')
# def top_rated_tv():
#     """
#     Affiche les séries TV les mieux notées
#     """
#     # Récupérer le paramètre de genre s'il existe
#     genre_filter = request.args.get('genre')
    
#     # Récupérer les séries TV les mieux notées
#     tv_data = get_top_rated_tv_shows()
#     tv_shows = tv_data.get('results', [])
    
#     # Récupérer les genres pour l'affichage
#     genres = get_tv_genres()
    
#     # Formater les séries TV pour l'affichage
#     formatted_tv_shows = format_tv_shows(tv_shows)
    
#     # Filtrer par genre si nécessaire
#     if genre_filter:
#         formatted_tv_shows = [show for show in formatted_tv_shows 
#                            if int(genre_filter) in show.get('genre_ids', [])]
    
#     return render_template('tv_shows.html', 
#                           tv_shows=formatted_tv_shows, 
#                           genres=genres,
#                           title="Séries TV les mieux notées", 
#                           genre_filter=genre_filter)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)
