import re

import bcrypt


def validate_username(username):
    # Regex pattern for username validation
    pattern = r"^[a-zA-Z0-9_-]{3,20}$"
    return re.match(pattern, username) is not None


def validate_email(email):
    # Regex pattern for email validation
    pattern = r"^[\w\.-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def hashing_password(password):
    salt = bcrypt.gensalt(rounds=12, prefix=b"2a")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password
