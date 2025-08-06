import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.services import facade

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        # create admin user for authentication
        admin = facade.create_user({
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@example.com',
            'password': 'adminpwd',
            'is_admin': True
        })
        login_res = self.client.post('/api/v1/login', json={'email': 'admin@example.com', 'password': 'adminpwd'})
        self.admin_token = login_res.get_json()['access_token']

    def test_create_user(self):
       response = self.client.post(
            '/api/v1/users/',
            headers={'Authorization': f'Bearer {self.admin_token}'},
            json={
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'jane.doe@example.com',
                'password': 'pwd'
            })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'Jane')

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email'
            })
        self.assertEqual(response.status_code, 400)

    def test_update_first_name(self):
        # create user directly via facade
        user = facade.create_user({
            'first_name': 'Old',
            'last_name': 'Name',
            'email': 'old@example.com',
            'password': 'pwd'
            })
        # authenticate to get a token
        login_res = self.client.post('/api/v1/login',
                                     json={'email': 'old@example.com',
                                           'password': 'pwd'})
        token = login_res.get_json()['access_token']
        # update first name only
        response = self.client.put(f'/api/v1/users/{user.id}',
                                   headers={'Authorization': f'Bearer {token}'},
                                   json={'first_name': 'New'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'New')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
