import strawberry
from bson import ObjectId

from database import db
from models.comment_model import UpdateCommentInput
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
        comment_obj = comment_collection.find_one(
            {
                "tweet_id": ObjectId(tweetId),
                "comment": {
                    "$elemMatch": {
                        "user_id": ObjectId(response["response"]["user_id"]),
                    }
                },
            }
        )
        if comment_obj:
            return GeneralResponse(msg="Comment already exists", success=False)
        # If the comment does not exist for the user, then add the comment
        comment_update_result = comment_collection.update_one(
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
        if not comment_update_result.modified_count > 0:
            return GeneralResponse(msg="Unable to add comment", success=False)
        return GeneralResponse(msg="Successfully Added Comment", success=True)

    @strawberry.mutation
    def update_comment(
        self, info, inputData: UpdateCommentInput
    ) -> GeneralResponse:
        inputData = inputData.to_dict()
        user_data = verify_user_token(token=inputData["token"])
        if not user_data["success"]:
            return GeneralResponse(
                msg="Authentication Failed: Invalid Token", success=False
            )
        tweet_obj = tweet_collection.find_one(
            {"_id": ObjectId(inputData["tweetId"])}
        )
        if not tweet_obj:
            return GeneralResponse(msg="Tweet Not Found", success=False)
        filter = {
            "tweet_id": ObjectId(inputData["tweetId"]),
            "comment.user_id": ObjectId(user_data["response"]["user_id"]),
        }
        update_query = {
            "$set": {"comment.$.description": inputData["comment"]}
        }
        comment_obj = comment_collection.update_one(filter, update_query)
        if not comment_obj.modified_count > 0:
            return GeneralResponse(
                msg="Unable to update comment", success=False
            )
        return GeneralResponse(
            msg="Successfully Updated Comment", success=True
        )

    @strawberry.mutation
    def delete_comment(
        self, info, token: str, tweetId: str
    ) -> GeneralResponse:
        user_data = verify_user_token(token=token)
        if not user_data["success"]:
            return GeneralResponse(
                msg="Authentication Failed: Invalid Token", success=False
            )
        tweet_obj = tweet_collection.find_one({"_id": ObjectId(tweetId)})
        if not tweet_obj:
            return GeneralResponse(msg="Tweet Not Found", success=False)
        delete_comment_obj = comment_collection.update_one(
            {"tweet_id": ObjectId(tweetId)},
            {
                "$pull": {
                    "comment": {
                        "user_id": ObjectId(user_data["response"]["user_id"])
                    }
                }
            },
        )
        if not delete_comment_obj.modified_count > 0:
            return GeneralResponse(
                msg="Unable to delete comment", success=False
            )
        return GeneralResponse(
            msg="Successfully Deleted Comment", success=True
        )
