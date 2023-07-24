import strawberry
from bson import ObjectId

from database import db
from models.user_model import GeneralResponse
from utility.user_utility import verify_user_token

tweet_collection = db["tweet"]
comment_collection = db["comment"]


@strawberry.type
class CommentMutattion:
    @strawberry.mutation
    def add_comment(
        self, info, token: str, tweetId: str, comment: str
    ) -> GeneralResponse:
        response = verify_user_token(token=token)
        if not response["success"]:
            return GeneralResponse(
                msg="Authentication Failed: Invalid Token", success=False
            )
        tweet_obj = tweet_collection.find_one({"_id": ObjectId(tweetId)})
        if not tweet_obj:
            return GeneralResponse(msg="Tweet Not Found", success=False)
        comment_obj = comment_collection.update_one(
            {"tweet_id": ObjectId(tweetId)},
            {
                "$addToSet": {
                    "comment": {
                        "user_id": ObjectId(response["response"]["user_id"]),
                        "description": comment,
                    }
                }
            },
        )
        if not comment_obj.modified_count > 0:
            return GeneralResponse(msg="Unable to add comment", success=False)
        return GeneralResponse(msg="Successfully Added Comment", success=True)
