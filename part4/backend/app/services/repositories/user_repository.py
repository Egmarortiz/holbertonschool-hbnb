from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository for ``User`` objects providing helpful query methods."""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retrieve a user by email address."""
        return self.model.query.filter_by(email=email).first()
