from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password')
    })

# Model used when updating an existing user. Admins may modify all fields,
# while regular users can only change their first and last names.
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='User password')
    })

@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email} for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                    'id': new_user.id,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'email': new_user.email,
                    'password': new_user.password,
                    }, 201
        except ValueError as e:
            return {'error': str(e)}, 400



@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retreived successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get usr details by id"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update a user's information"""
        user_data = api.payload or {}
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        current_id = current_user['id'] if isinstance(current_user, dict) else current_user

        if not is_admin and user_id != current_id:
            return {'error': 'Unauthorized action'}, 403

        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password'}, 400

        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Check if email is being changed and if new email is already taken
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400

        # Update the user
        updated_user = facade.update_user(user_id, user_data)
        return {'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email}, 200
