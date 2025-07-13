import os
from app import create_app
from app.services import facade

app = create_app()

def seed_admin():
    """Create a default administrator if none exists."""
    email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    password = os.getenv('ADMIN_PASSWORD', 'admin')
    if not facade.get_user_by_email(email):
        facade.create_user({
            'first_name': 'Admin',
            'last_name': 'User',
            'email': email,
            'password': password,
            'is_admin': True,
        })

if __name__ == '__main__':
    seed_admin()
    app.run(host='0.0.0.0', port=5000, debug=True)
