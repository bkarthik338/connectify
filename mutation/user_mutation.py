# File contains the Class for POST/UPDATE
import strawberry

from database import db
from utility.user_utility import hashing_password
from utility.user_utility import validate_email
from utility.user_utility import validate_username

user_collection = db["user"]


@strawberry.type
class CreateUserResposne:
    success: bool
    msg: str


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(
        self, info, username: str, email: str, password: str
    ) -> CreateUserResposne:
        if user_collection.find_one({"username": username}):
            return CreateUserResposne(
                msg=f"Username Already Exists: {username}", success=False
            )
        if not validate_email(email=email):
            return CreateUserResposne(
                msg=f"Invalid Email: {email}", success=False
            )
        if not validate_username(username=username):
            return CreateUserResposne(
                msg=f"Invalid Username: {username}", success=False
            )
        hashed_password = hashing_password(password)
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
        }
        _ = user_collection.insert_one(user_data)
        return CreateUserResposne(
            msg=f"User created Successfully: {username}", success=True
        )
