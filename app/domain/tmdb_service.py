import os
import requests
from flask import Blueprint, jsonify
from app.models import db, Movie
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv('API_KEY')
TMDB_API_URL = "https://api.themoviedb.org/3"

tmdb_bp = Blueprint('tmdb', __name__)

def fetch_popular_movies():
    response = requests.get(f"{TMDB_API_URL}/movie/popular", params={
        "api_key": TMDB_API_KEY,
        "language": "fr-FR",
        "page": 1
    })
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

@tmdb_bp.route("/sync", methods=["GET"])
def sync_movies():
    movies = fetch_popular_movies()

    for movie in movies:
        existing = Movie.query.filter_by(tmdb_id=movie["id"]).first()
        if not existing:
            new_movie = Movie(
                tmdb_id=movie["id"],
                title=movie["title"],
                overview=movie["overview"],
                release_date=movie.get("release_date", ""),
                vote_average=movie.get("vote_average", 0),
                poster_path=movie.get("poster_path", ""),
                genre_ids=movie.get("genre_ids", [])
            )
            db.session.add(new_movie)
    db.session.commit()
    return jsonify({"message": "Films synchronisés avec succès"}), 200
