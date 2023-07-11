import os
import re

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

secret_key = os.environ.get("SECRET_JWT_KEY")
algorithm = os.environ.get("JWT_ALGORITHM")


def validate_username(username: str) -> bool:
    # Regex pattern for username validation
    pattern = r"^[a-zA-Z0-9_-]{3,20}$"
    return re.match(pattern, username) is not None


def validate_email(email: str) -> bool:
    # Regex pattern for email validation
    pattern = r"^[\w\.-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def hashing_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12, prefix=b"2a")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def generate_jwt_token(payload: dict) -> str:
    """
    payload: Dict
    ex: {"user_id": 123, "exp": 1630425600}
    """
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def verify_user_token(token: str) -> dict:
    """
    Verifying User token
    ex: "dasdadfsddfsdf......"
    """
    try:
        decoded_data = jwt.decode(token, secret_key, algorithms=algorithm)
        return {"response": decoded_data, "success": True}
    except jwt.ExpiredSignatureError:
        return {"response": "Token has expired", "success": False}
    except jwt.InvalidTokenError:
        return {"response": "Invalid Token", "success": False}
