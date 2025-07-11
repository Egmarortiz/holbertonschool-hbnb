import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.services import facade

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()
        # Prepare user, amenity, place
        self.user = facade.create_user({
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com'
        })
        self.place = facade.create_place({
            'title': 'House',
            'description': '',
            'price': 80,
            'latitude': 0.0,
            'longitude': 0.0,
            'owner_id': self.user.id,
            'amenities': []
        })

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Great',
            'rating': 5,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['rating'], 5)

    def test_create_review_empty_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            'text': '',
            'rating': 3,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
