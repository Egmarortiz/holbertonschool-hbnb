from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        # Relationship
        self.places = []  # List of Place instances

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value or len(value) > 50:
            raise ValueError("name must be a non-empty string up to 50 characters")
        self._name = value
