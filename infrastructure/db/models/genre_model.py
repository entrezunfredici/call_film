from infrastructure.db.database import db

class GenreModel(db.Model):
    """Modèle SQLAlchemy pour un genre de film"""
    __tablename__ = 'genre'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"<Genre {self.name}>"
