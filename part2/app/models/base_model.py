import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """Update the `updated_at` timestamp."""
        self.updated_at = datetime.utcnow()

    def update(self, data: dict):
        """Update attributes from a dict and refresh timestamp."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Serialize to dict with ISO timestamps."""
        result = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result
