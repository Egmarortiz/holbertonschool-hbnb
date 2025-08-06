import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.services import facade

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        # Prepare owner and reviewer
        owner = facade.create_user({
            'first_name': 'Owner',
            'last_name': 'One',
            'email': 'owner@example.com',
            'password': 'pwd'
            })
        reviewer = facade.create_user({
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'password': 'pwd'
            })
        self.place = facade.create_place({
            'title': 'House',
            'description': '',
            'price': 80,
            'latitude': 0.0,
            'longitude': 0.0,
            'owner_id': owner.id,
            'amenities': []
            })

        login_res = self.client.post(
                '/api/v1/login',
                json={'email': 'alice@example.com', 'password': 'pwd'}
                )
        self.token = login_res.get_json()['access_token']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_review(self):
        response = self.client.post(
                '/api/v1/reviews/',
                headers={'Authorization': f'Bearer {self.token}'},
                json={
                    'text': 'Great',
                    'rating': 5,
                    'place_id': self.place.id
                    }
                )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['rating'], 5)

    def test_create_review_empty_text(self):
        response = self.client.post(
                '/api/v1/reviews/',
                headers={'Authorization': f'Bearer {self.token}'},
                json={
                    'text': '',
                    'rating': 3,
                    'place_id': self.place.id
                    }
                )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
