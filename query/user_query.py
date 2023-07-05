# File contains the query class functions GET
import strawberry
from bson import ObjectId

from database import db
from model import User

user_collection = db["user"]


@strawberry.type
class GetUserResponse:
    data: User
    success: bool


@strawberry.type
class GetUserFailureResponse:
    error: str
    success: bool


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
