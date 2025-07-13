from app import db
from .base_model import BaseModel


class Review(BaseModel):
    """SQLAlchemy model for reviews."""

    __tablename__ = "reviews"

    text = db.Column("comment", db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'))
    user = db.relationship('User', backref='reviews')
    place = db.relationship('Place', back_populates='reviews')

    def __init__(self, user=None, place=None, rating=0, comment="", **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.place = place
        self.rating = rating
        self.text = comment
        self.validate()

    def validate(self):
        if not self.text.strip():
            raise ValueError("Review text cannot be empty")
