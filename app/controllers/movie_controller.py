from flask import Blueprint, render_template, request
from services.tmdb_service import get_now_playing_movies, get_movie_genres, format_movies

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/now-playing')
def now_playing():
    now_playing = get_now_playing_movies()
    movies = now_playing.get("results", [])
    genres = get_movie_genres()
    genre_id = request.args.get('genre', type=int)
    if genre_id:
        movies = [m for m in movies if genre_id in m.get("genre_ids", [])]
    movies = format_movies(movies)
    return render_template('movies.html', 
                           movies=movies, 
                           genres=genres, 
                           selected_genre=genre_id, 
                           title="Films actuellement au cinéma",
                           active_page="now-playing")
