# File contains the Class for POST/UPDATE
import strawberry
from bson import ObjectId

from database import db
from models.user_model import CreateUserResponse
from models.user_model import DeleteUserResponse
from utility.user_utility import hashing_password
from utility.user_utility import validate_email
from utility.user_utility import validate_username

user_collection = db["user"]


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(
        self, info, username: str, email: str, password: str
    ) -> CreateUserResponse:
        print("db:\n", db)
        if user_collection.find_one({"username": username}):
            return CreateUserResponse(
                msg=f"Username Already Exists: {username}", success=False
            )
        print("Username Check is done")
        if not validate_email(email=email):
            return CreateUserResponse(
                msg=f"Invalid Email: {email}", success=False
            )
        if not validate_username(username=username):
            return CreateUserResponse(
                msg=f"Invalid Username: {username}", success=False
            )
        hashed_password = hashing_password(password)
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
        }
        _ = user_collection.insert_one(user_data)
        return CreateUserResponse(
            msg=f"User created Successfully: {username}", success=True
        )

    @strawberry.mutation
    def delete_user(
        self, info, username: str = None, id: strawberry.ID = None
    ) -> DeleteUserResponse:
        query = {"_id": ObjectId(id)} if id else {"username": username}
        if not user_collection.find_one(query):
            return DeleteUserResponse(
                msg="User is not registered to delete.", success=False
            )
        _ = user_collection.delete_one(query)
        return DeleteUserResponse(msg="User is deleted.", success=True)
