import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.services import facade

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        # Create a user and amenity to reference
        self.user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'pwd'
        })
        self.amenity = facade.create_amenity({'name': 'Wifi'})

        # Authenticate user to get JWT
        login_res = self.client.post(
            '/api/v1/login',
            json={'email': 'john@example.com', 'password': 'pwd'}
        )
        self.token = login_res.get_json()['access_token']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_place(self):
        response = self.client.post(
            '/api/v1/places/',
            headers={'Authorization': f'Bearer {self.token}'},
            json={
                'title': 'Nice Place',
                'description': 'Cozy',
                'price': 100,
                'latitude': 10.0,
                'longitude': 20.0,
                'amenities': [self.amenity.id]
            }
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], 'Nice Place')

    def test_create_place_invalid_latitude(self):
        response = self.client.post(
            '/api/v1/places/',
            headers={'Authorization': f'Bearer {self.token}'},
            json={
                'title': 'Bad Place',
                'price': 50,
                'latitude': 100.0,
                'longitude': 0.0,
                'amenities': []
            }
        )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
