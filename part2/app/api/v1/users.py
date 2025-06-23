from flask_restx import Namespace, Resource, fields
from app.services import HBNB_FACADE

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'id': fields.String(readonly=True, description='ID'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

    @api.marshall_list_with(user_model)
    def get(self):
        return HBNB_FACADE_repo.get_all()

@api.route('/<string:id>')
class UserResource(Resource):
    @api.marshal_with(user_modeli)
    def get(self, id):
        return HBNB_FACADE.get_user(id)

    def delete(self, id):
        HBNB_FACADE.user_repo.delete(id)
        return '', 204

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, id):
        return HBNB_FACADE.update_user(id, api.payload)
