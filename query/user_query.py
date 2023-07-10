# File contains the query class functions GET
import bcrypt
import strawberry
from bson import ObjectId

from database import db
from models.user_model import GetUserFailureResponse
from models.user_model import GetUserResponse
from models.user_model import LoginResponse
from models.user_model import User
from utility.user_utility import generate_jwt_token

user_collection = db["user"]


@strawberry.type
class UserQuery:
    @strawberry.field
    def getuser(
        self, info, id: strawberry.ID = None, username: str = None
    ) -> strawberry.union(
        "getUserFieldUnion", [GetUserResponse, GetUserFailureResponse]
    ):
        query = {"_id": ObjectId(id)} if id else {"username": username}
        user_data = user_collection.find_one(query)
        if user_data:
            return GetUserResponse(
                data=User(
                    id=str(user_data["_id"]),
                    username=user_data["username"],
                    email=user_data["email"],
                ),
                success=True,
            )
        return GetUserFailureResponse(
            error=f"Invalid User id: {id} or username: {username}",
            success=False,
        )

    @strawberry.field
    def userlogin(self, info, username: str, password: str) -> LoginResponse:
        user_data = user_collection.find_one({"username": username})
        if not user_data:
            return LoginResponse(
                msg=f"Login Failure Invalid Username: {username}",
                success=False,
            )
        if not bcrypt.checkpw(password.encode("utf-8"), user_data["password"]):
            return LoginResponse(
                msg="Invalid Username/Password", success=False
            )
        generated_token = generate_jwt_token(
            {"user_id": str(user_data["_id"])}
        )
        return LoginResponse(
            msg="Login Successful", success=True, token=generated_token
        )
