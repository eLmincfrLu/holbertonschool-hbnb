from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.models.user import User

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/login')
class LoginResource(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        data = api.payload
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.verify_password(data['password']):
            # IDENTITY MÜTLƏQ STRİNG OLMALIDIR (user.id)
            # Digər məlumatları (məs: is_admin) additional_claims ilə göndəririk
            access_token = create_access_token(
                identity=user.id, 
                additional_claims={'is_admin': user.is_admin}
            )
            return {'access_token': access_token}, 200
            
        return {'error': 'Invalid credentials'}, 401