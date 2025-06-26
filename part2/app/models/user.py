from .base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name="", last_name="", email="", password=""):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.places = []
        self.validate()

    def validate(self):
        if not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if not self.email or "@" not in self.email or "." not in self.email:
            raise ValueError("Invalid email format")

    def add_place(self, place):
        if place and place.owner == self:
            self.places.append(place)
