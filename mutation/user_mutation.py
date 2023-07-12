# File contains the Class for POST/UPDATE
import bcrypt
import strawberry
from bson import ObjectId

from constants import UPDATE_USER_TABLE_KEYS
from database import db
from models.user_model import GeneralResponse
from models.user_model import UpdateUserInput
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
    ) -> GeneralResponse:
        if user_collection.find_one({"username": username}):
            return GeneralResponse(
                msg=f"Username Already Exists: {username}", success=False
            )
        print("Username Check is done")
        if not validate_email(email=email):
            return GeneralResponse(
                msg=f"Invalid Email: {email}", success=False
            )
        if not validate_username(username=username):
            return GeneralResponse(
                msg=f"Invalid Username: {username}", success=False
            )
        hashed_password = hashing_password(password)
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
        }
        _ = user_collection.insert_one(user_data)
        return GeneralResponse(
            msg=f"User created Successfully: {username}", success=True
        )

    @strawberry.mutation
    def delete_user(
        self, info, username: str = None, id: strawberry.ID = None
    ) -> GeneralResponse:
        query = {"_id": ObjectId(id)} if id else {"username": username}
        if not user_collection.find_one(query):
            return GeneralResponse(
                msg="User is not registered to delete.", success=False
            )
        _ = user_collection.delete_one(query)
        return GeneralResponse(msg="User is deleted.", success=True)

    @strawberry.mutation
    def update_user(
        self, info, token: str, user_input: UpdateUserInput
    ) -> GeneralResponse:
        response = verify_user_token(token=token)
        if not response["success"]:
            return GeneralResponse(msg=response["response"], success=False)
        update_dict = {}
        update_data = user_input.to_dict()
        for key, value in update_data.items():
            if key in UPDATE_USER_TABLE_KEYS and value is not None:
                update_dict[key] = value
        if not update_dict:
            return GeneralResponse(
                msg="Invalid data sent for updation", success=False
            )
        query = {"_id": ObjectId(response["response"]["user_id"])}
        updated_obj = user_collection.update_one(query, {"$set": update_dict})
        if not updated_obj.modified_count > 0:
            return GeneralResponse(msg="User Updation Failed", success=False)
        return GeneralResponse(msg="Updated User Successfully", success=True)

    @strawberry.mutation
    def reset_password(
        self, info, token: str, oldPassword: str, newPassword: str
    ) -> GeneralResponse:
        response = verify_user_token(token=token)
        if not response["success"]:
            return GeneralResponse(msg="Invalid Token", success=False)
        if newPassword == oldPassword:
            return GeneralResponse(
                msg="New Password Should Not Be Same As Old Password",
                success=False,
            )
        query = {"_id": ObjectId(response["response"]["user_id"])}
        user_data = user_collection.find_one(query)
        if not bcrypt.checkpw(
            oldPassword.encode("utf-8"), user_data["password"]
        ):
            return GeneralResponse(
                msg="Old Password Entered Is Incorrect", success=False
            )
        hashed_password = hashing_password(newPassword)
        user_update_obj = user_collection.update_one(
            query, {"$set": {"password": hashed_password}}
        )
        if not user_update_obj.modified_count > 0:
            return GeneralResponse(
                msg="Password Updation Failed", success=False
            )
        return GeneralResponse(
            msg="Successfully Updated Password", success=True
        )
