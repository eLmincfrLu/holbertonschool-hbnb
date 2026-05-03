from app.models.base import BaseModel
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = bcrypt.generate_password_hash(kwargs['password']).decode('utf-8')
        super().__init__(**kwargs)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
