from flask import Blueprint, render_template, request
from app.domain.tmdb_service import get_now_playing_movies, get_movie_genres, format_movies

movie_bp = Blueprint('movie', __name__)

@app.route('/movies')
def movies_from_db():
    genre_id = request.args.get('genre', type=int)
    query = Movie.query
    if genre_id:
        query = query.filter(Movie.genre_ids.any(genre_id))

    movies = query.all()
    for m in movies:
        m.poster_url = f"https://image.tmdb.org/t/p/w500{m.poster_path}" if m.poster_path else "/static/no-poster.jpg"

    genres = get_movie_genres()  # ou bien tu stockes aussi les genres en DB

    return render_template("movies.html", movies=movies, genres=genres, selected_genre=genre_id, title="Films")
