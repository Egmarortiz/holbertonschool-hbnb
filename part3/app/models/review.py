from app import db
from .base_model import BaseModel


class Review(BaseModel):
    """SQLAlchemy model for reviews."""

    __tablename__ = "reviews"

    text = db.Column("comment", db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, user=None, place=None, rating=0, comment="", **kwargs):
        super().__init__(**kwargs)
        self.user = user  # reference to the user who wrote the review
        self.place = place  # reference to the place being reviewed        self.rating = rating
        self.text = comment
        self.validate()

    def validate(self):
        if not self.text.strip():
            raise ValueError("Review text cannot be empty")
