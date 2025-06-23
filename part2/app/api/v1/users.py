from flask_restx import Namespace, Resource, fields
from app.services import HBNB_FACADE

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readonly=True, description='ID'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return HBNB_FACADE.user_repo.get_all()

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        return HBNB_FACADE.create_user(api.payload), 201

@api.route('/<string:id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, id):
        return HBNB_FACADE.get_user(id)

    def delete(self, id):
        HBNB_FACADE.user_repo.delete(id)
        return '', 204

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, id):
        return HBNB_FACADE.update_user(id, api.payload)
