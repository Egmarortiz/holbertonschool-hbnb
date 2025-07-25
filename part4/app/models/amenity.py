from app import db
from .base_model import BaseModel


class Amenity(BaseModel):

    """SQLAlchemy model for amenities."""

    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name="", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.validate()

    def validate(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
