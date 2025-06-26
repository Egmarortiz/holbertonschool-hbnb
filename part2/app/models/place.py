from .base_model import BaseModel


class Place(BaseModel):
    def __init__(self, name="", description="", price=0, latitude=0.0,
                 longitude=0.0, owner=None):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
        self.validate()

    def add_reviews(self, review):
        if review and review.place == self:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def validate(self):
        if not self.name.strip():
            raise ValueError("Title cannot be empty")
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(self.latitude, (int, float)) or not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not isinstance(self.longitude, (int, float)) or not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
