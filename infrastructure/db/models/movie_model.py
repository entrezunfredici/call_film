from infrastructure.db.database import db
from sqlalchemy.ext.associationproxy import association_proxy

# Table d'association pour la relation many-to-many entre Movie et Genre
movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class MovieModel(db.Model):
    """Modèle SQLAlchemy pour un film"""
    __tablename__ = 'movie'
    
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    overview = db.Column(db.Text)
    release_date = db.Column(db.String(20))
    vote_average = db.Column(db.Float)
    poster_path = db.Column(db.String(255))
    
    # Relation many-to-many avec les genres
    genres = db.relationship('GenreModel', secondary=movie_genres, 
                           backref=db.backref('movies', lazy='dynamic'))
    
    # Proxy pour accéder directement aux IDs des genres
    genre_ids = association_proxy('genres', 'id')
    
    def __repr__(self):
        return f"<Movie {self.title}>"
