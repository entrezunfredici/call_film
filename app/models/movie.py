from app.extensions import db
from .genre import Genre

movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255))
    overview = db.Column(db.Text)
    release_date = db.Column(db.String(20))
    vote_average = db.Column(db.Float)
    poster_path = db.Column(db.String(255))
    genres_ids = db.relationship('Genre', secondary=movie_genres, backref='movies')