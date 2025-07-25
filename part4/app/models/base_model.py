import uuid
from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base class for all SQLAlchemy models in the application."""

    __abstract__ = True  # SQLAlchemy will not create a table for this class

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()


    def save(self):
        """Persist the current instance to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update attributes on the model instance and persist changes."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
