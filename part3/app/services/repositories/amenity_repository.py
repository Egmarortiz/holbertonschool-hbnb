from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Repository for ``Place`` objects."""

    def __init__(self):
        super().__init__(Place)
