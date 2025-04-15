# app.py
from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'une_clé_secrète_par_défaut')

# Configuration de l'API TMDB
TMDB_API_KEY = os.getenv('API_KEY')
TMDB_API_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

def get_now_playing_movies():
    """Récupère les films actuellement en salle"""
    endpoint = f"{TMDB_API_URL}/movie/now_playing"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "fr-FR",
        "page": 1
    }
    
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"results": []}

def get_popular_movies():
    """Récupère les films les plus populaires"""
    endpoint = f"{TMDB_API_URL}/movie/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "fr-FR",
        "page": 1
    }
    
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"results": []}

def search_movies(query):
    """Recherche des films par nom"""
    endpoint = f"{TMDB_API_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "fr-FR",
        "query": query,
        "page": 1
    }
    
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"results": []}

def get_movie_genres():
    """Récupère la liste des genres de films"""
    endpoint = f"{TMDB_API_URL}/genre/movie/list"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "fr-FR"
    }
    
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        return response.json()["genres"]
    else:
        return []

def format_movies(movies):
    """Formate les données des films pour l'affichage"""
    for movie in movies:
        if movie.get("poster_path"):
            movie["poster_url"] = f"{POSTER_BASE_URL}{movie['poster_path']}"
        else:
            movie["poster_url"] = "/static/no-poster.jpg"
    return movies

@app.route('/')
def home():
    """Page d'accueil avec les boutons de navigation"""
    return render_template('home.html')

@app.route('/now-playing')
def now_playing():
    """Page des films en salle"""
    # Récupération des films en salle
    now_playing = get_now_playing_movies()
    movies = now_playing.get("results", [])
    
    # Récupération des genres
    genres = get_movie_genres()
    
    # Création d'un dictionnaire pour faciliter l'accès aux noms des genres
    genre_dict = {genre["id"]: genre["name"] for genre in genres}
    
    # Filtre par genre si spécifié
    genre_id = request.args.get('genre', type=int)
    if genre_id:
        movies = [movie for movie in movies if genre_id in movie.get("genre_ids", [])]
    
    # Ajout de l'URL complète des posters
    movies = format_movies(movies)
    
    return render_template('movies.html', 
                          movies=movies, 
                          genres=genres, 
                          selected_genre=genre_id, 
                          title="Films actuellement au cinéma",
                          active_page="now-playing")

@app.route('/popular')
def popular():
    """Page des films populaires"""
    # Récupération des films populaires
    popular_data = get_popular_movies()
    movies = popular_data.get("results", [])
    
    # Récupération des genres
    genres = get_movie_genres()
    
    # Filtre par genre si spécifié
    genre_id = request.args.get('genre', type=int)
    if genre_id:
        movies = [movie for movie in movies if genre_id in movie.get("genre_ids", [])]
    
    # Ajout de l'URL complète des posters
    movies = format_movies(movies)
    
    return render_template('movies.html', 
                          movies=movies, 
                          genres=genres, 
                          selected_genre=genre_id, 
                          title="Films populaires",
                          active_page="popular")

@app.route('/search')
def search():
    """Page de recherche de films"""
    query = request.args.get('query', '')
    
    if not query:
        return render_template('search.html', movies=[], query='')
    
    # Recherche des films
    search_results = search_movies(query)
    movies = search_results.get("results", [])
    
    # Récupération des genres
    genres = get_movie_genres()
    
    # Filtre par genre si spécifié
    genre_id = request.args.get('genre', type=int)
    if genre_id:
        movies = [movie for movie in movies if genre_id in movie.get("genre_ids", [])]
    
    # Ajout de l'URL complète des posters
    movies = format_movies(movies)
    
    return render_template('search.html', 
                          movies=movies, 
                          genres=genres, 
                          selected_genre=genre_id, 
                          query=query,
                          active_page="search")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
