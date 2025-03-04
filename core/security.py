import bcrypt
import jwt
import datetime
from config import settings

SECRET_KEY = settings.secret_key  # Load secret key from settings
ALGORITHM = "HS256"
TOKEN_EXPIRATION = 60 * 60  # 1 hour

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if a plain password matches the hashed password"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    """Generates a JWT token"""
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_EXPIRATION)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
