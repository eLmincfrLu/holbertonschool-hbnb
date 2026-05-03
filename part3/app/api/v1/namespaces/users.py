from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app import db

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_admin': fields.Boolean(default=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        data = api.payload
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already registered'}, 400
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return {'id': new_user.id, 'email': new_user.email}, 201

@api.route('/me')
class UserMe(Resource):
    @jwt_required()
    def get(self):
        # Artıq get_jwt_identity() bizə birbaşa user_id stringini qaytaracaq
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id, 
            'email': user.email, 
            'first_name': user.first_name,
            'last_name': user.last_name
        }, 200