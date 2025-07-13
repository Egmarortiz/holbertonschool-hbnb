from app import create_app
from app.services import facade

app = create_app()  # initializes Flask and other extensions

# create the administrator
facade.create_user({
    'first_name': 'Admin',
    'last_name': 'User',
    'email': 'admin@example.com',
    'password': 'adminpwd',
    'is_admin': True
})
