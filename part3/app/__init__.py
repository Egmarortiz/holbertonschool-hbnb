from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import config

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Ensure tables exist each time the app starts
    with app.app_context():
        db.create_all()

    from app.api.v1.users import api as users_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # API namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
