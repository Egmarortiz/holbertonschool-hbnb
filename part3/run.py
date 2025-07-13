from app import create_app
from app.services import facade

app = create_app()

with app.app_context():
    # Only seed if not already present
    try:
        facade.get_user_by_email("admin@example.com")
    except KeyError:  # or whatever your “not found” error is
        facade.create_user({
            'first_name': 'Admin',
            'last_name':  'User',
            'email':      'admin@example.com',
            'password':   'adminpwd',
            'is_admin':   True
        })
        print("✅ Seeded in-memory admin user")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
