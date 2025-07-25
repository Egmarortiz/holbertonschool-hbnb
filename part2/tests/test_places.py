import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.services import facade

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        # Create a user and amenity to reference
        self.user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        })
        self.amenity = facade.create_amenity({'name': 'Wifi'})

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            'title': 'Nice Place',
            'description': 'Cozy',
            'price': 100,
            'latitude': 10.0,
            'longitude': 20.0,
            'owner_id': self.user.id,
            'amenities': [self.amenity.id]
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], 'Nice Place')

    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            'title': 'Bad Place',
            'price': 50,
            'latitude': 100.0,
            'longitude': 0.0,
            'owner_id': self.user.id,
            'amenities': []
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
