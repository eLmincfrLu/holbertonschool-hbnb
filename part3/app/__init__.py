from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

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

    from app.api.v1.namespaces.users import api as users_ns
    from app.api.v1.namespaces.auth import api as auth_ns
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
