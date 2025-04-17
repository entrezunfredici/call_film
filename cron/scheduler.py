from apscheduler.schedulers.background import BackgroundScheduler
from app.domain.tmdb_service import fetch_popular_movies
from app.extensions import db
from app.models.movie import Movie
from flask import Flask
import os

def create_scheduler(app):
    def job():
        with app.app_context():
            print("⏱️ Synchronisation des films...")
            movies = fetch_popular_movies()
            for movie in movies:
                if not Movie.query.filter_by(tmdb_id=movie["id"]).first():
                    db.session.add(Movie(
                        tmdb_id=movie["id"],
                        title=movie["title"],
                        overview=movie["overview"],
                        release_date=movie.get("release_date", ""),
                        vote_average=movie.get("vote_average", 0),
                        poster_path=movie.get("poster_path", ""),
                        genre_ids=movie.get("genre_ids", [])
                    ))
            db.session.commit()

    interval = int(os.getenv("SYNC_INTERVAL_MINUTES", 60))
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', minutes=interval)
    scheduler.start()