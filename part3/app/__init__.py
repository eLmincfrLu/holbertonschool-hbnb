from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

# Obyektləri funksiyadan kənarda yaradın ki, hər yerdən əlçatan olsun
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # 1. Mütləq CORS-u aktivləşdiririk (Front-end ilə rabitə üçün)
    CORS(app)
    
    # 2. Konfiqurasiyanı yükləyirik
    app.config.from_object(config[config_name])

    # 3. İnitalize obyektlər
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Bura belə yazın: Bearer <SƏNİN_TOKENİN>"
        }
    }

    api = Api(app, 
              version='1.0', 
              title='HBnB API', 
              description='HBnB Part 3 with Database',
              authorizations=authorizations,
              security='apikey'
    )

    # Namespace-ləri əlavə edin
    from app.api.v1.namespaces.users import api as users_ns
    from app.api.v1.namespaces.auth import api as auth_ns
    from app.api.v1.namespaces.places import api as places_ns  # Mütləq əlavə et
    from app.api.v1.namespaces.reviews import api as reviews_ns # Mütləq əlavə et
    from app.api.v1.namespaces.amenities import api as amenities_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app