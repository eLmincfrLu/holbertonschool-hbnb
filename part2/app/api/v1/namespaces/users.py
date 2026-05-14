from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        user_data = api.payload
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400
        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

    def get(self):
        users = facade.get_all_users()
        return [{'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} for u in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user: return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    def put(self, user_id):
        updated_user = facade.update_user(user_id, api.payload)
        if not updated_user: return {'error': 'User not found'}, 404
        return {'message': 'User updated successfully'}, 200
