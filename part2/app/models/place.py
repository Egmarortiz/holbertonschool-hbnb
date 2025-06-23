from .base_model import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self,
                 title: str,
                 description: str,
                 price: float,
                 latitude: float,
                 longitude: float,
                 owner: User):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")
        self.owner = owner
        owner.places.append(self)
        # Relationships
        self.amenities = []  # List of Amenity instances
        self.reviews = []    # List of Review instances

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value or len(value) > 100:
            raise ValueError("title must be a non-empty string up to 100 characters")
        self._title = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if value is not None and not isinstance(value, str):
            raise ValueError("description must be a string if provided")
        self._description = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("price must be a positive number")
        self._price = float(value)

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        if not isinstance(value, (int, float)) or not -90.0 <= value <= 90.0:
            raise ValueError("latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        if not isinstance(value, (int, float)) or not -180.0 <= value <= 180.0:
            raise ValueError("longitude must be between -180 and 180")
        self._longitude = float(value)

    def add_amenity(self, amenity):
        from .amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            amenity.places.append(self)

    def add_review(self, review):
        from .review import Review
        if not isinstance(review, Review):
            raise ValueError("review must be a Review instance")
        self.reviews.append(review)
