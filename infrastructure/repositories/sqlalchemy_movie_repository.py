from typing import List, Optional
from domain.entities.genre import Genre
from domain.repositories.genre_repository import GenreRepository
from infrastructure.db.database import db
from infrastructure.db.models.genre_model import GenreModel

class SqlAlchemyGenreRepository(GenreRepository):
    """Implémentation SQLAlchemy du repository de genres"""
    
    def _to_entity(self, model: GenreModel) -> Genre:
        """Convertit un modèle SQLAlchemy en entité de domaine"""
        return Genre(
            id=model.id,
            name=model.name
        )
    
    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        model = GenreModel.query.get(genre_id)
        return self._to_entity(model) if model else None
    
    def get_all(self) -> List[Genre]:
        models = GenreModel.query.all()
        return [self._to_entity(model) for model in models]
    
    def save(self, genre: Genre) -> Genre:
        # Vérifier si le genre existe déjà
        existing = GenreModel.query.get(genre.id)
        
        if existing:
            # Mise à jour
            existing.name = genre.name
            model = existing
        else:
            # Création
            model = GenreModel(
                id=genre.id,
                name=genre.name
            )
            db.session.add(model)
        
        db.session.commit()
        return self._to_entity(model)
