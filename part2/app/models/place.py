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
        self.owner = owner  # usr objct ref
        self.reviews = []  # lst reviews objct
        self.amenities = []  # lst amen objct

    def add_reviews(self, review):
        if review and review.place == self:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)
