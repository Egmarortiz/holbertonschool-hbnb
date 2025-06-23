import re
from .base_model import BaseModel

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        # Relationships
        self.places = []     # List of Place instances owned
        self.reviews = []    # List of Review instances written

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not isinstance(value, str) or not value or len(value) > 50:
            raise ValueError("first_name must be a non-empty string up to 50 characters")
        self._first_name = value

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not isinstance(value, str) or not value or len(value) > 50:
            raise ValueError("last_name must be a non-empty string up to 50 characters")
        self._last_name = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if not isinstance(value, str) or not EMAIL_REGEX.match(value):
            raise ValueError("email must be a valid email address")
        self._email = value
