from app import db
from .genre import Genre

movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.String(50))
    vote_average = db.Column(db.Float)
    overview = db.Column(db.Text)
    poster_url = db.Column(db.String(500))
    genres = db.relationship('Genre', secondary=movie_genres, backref='movies')
