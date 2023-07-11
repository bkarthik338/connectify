# File contains the Class for POST/UPDATE
import strawberry
from bson import ObjectId

from constants import UPDATE_USER_TABLE_KEYS
from database import db
from models.user_model import CreateUserResponse
from models.user_model import DeleteUserResponse
from models.user_model import UpdateUserInput
from models.user_model import UpdateUserResponse
from utility.user_utility import hashing_password
from utility.user_utility import validate_email
from utility.user_utility import validate_username
from utility.user_utility import verify_user_token

user_collection = db["user"]


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(
        self, info, username: str, email: str, password: str
    ) -> CreateUserResponse:
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

    @strawberry.mutation
    def update_user(
        self, info, token: str, user_input: UpdateUserInput
    ) -> UpdateUserResponse:
        response = verify_user_token(token=token)
        if not response["success"]:
            return UpdateUserResponse(msg=response["response"], success=False)
        update_dict = {}
        update_data = user_input.to_dict()
        for key, value in update_data.items():
            if key in UPDATE_USER_TABLE_KEYS and value is not None:
                update_dict[key] = value
        if not update_dict:
            return UpdateUserResponse(
                msg="Invalid data sent for updation", success=False
            )
        query = {"_id": ObjectId(response["response"]["user_id"])}
        updated_obj = user_collection.update_one(query, {"$set": update_dict})
        if not updated_obj.modified_count > 0:
            return UpdateUserResponse(
                msg="User Updation Failed", success=False
            )
        return UpdateUserResponse(
            msg="Updated User Successfully", success=True
        )
