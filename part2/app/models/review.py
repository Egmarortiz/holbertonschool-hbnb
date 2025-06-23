from .base_model import BaseModel
from .place import Place
from .user import User

class Review(BaseModel):
    def __init__(self, text: str, rating: int, place: Place, user: User):
        super().__init__()
        self.text = text
        self.rating = rating
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        self.place = place
        place.reviews.append(self)
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")
        self.user = user
        user.reviews.append(self)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if not isinstance(value, str) or not value:
            raise ValueError("text must be a non-empty string")
        self._text = value

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        self._rating = value
