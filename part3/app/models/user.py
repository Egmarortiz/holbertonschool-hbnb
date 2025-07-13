from app import db, bcrypt
from .base_model import BaseModel


class User(BaseModel):
    """User model mapped to the ``users`` table."""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = db.relationship(
        'Place',
        back_populates='owner',
        cascade='all, delete-orphan'
    )

    def __init__(self, first_name="", last_name="", email="", password="", is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
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

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
