import strawberry
from bson import ObjectId

from database import db
from models.user_model import GeneralResponse
from mutation.tweet_mutation import tweet_collection
from utility.user_utility import verify_user_token

likes_collection = db["like"]


@strawberry.type
class LikesMutattion:
    @strawberry.mutation
    def like_tweet(self, info, token: str, tweet_id: str) -> GeneralResponse:
        user_data = verify_user_token(token=token)
        if not user_data["success"]:
            return GeneralResponse(
                msg="Authentication Failed: Token Invalid", success=False
            )
        tweet_obj = tweet_collection.find_one({"_id": ObjectId(tweet_id)})
        if not tweet_obj:
            return GeneralResponse(msg="Tweet Not Found", success=False)
        like_obj = likes_collection.update_one(
            {"tweet_id": ObjectId(tweet_id)},
            {
                "$addToSet": {
                    "user_id": ObjectId(user_data["response"]["user_id"])
                }
            },
        )
        if not like_obj.modified_count > 0:
            return GeneralResponse(
                msg="Unable to dislike tweet", success=False
            )
        return GeneralResponse(msg="Liked The Tweet", success=True)

    @strawberry.mutation
    def dislike_tweet(
        self, info, token: str, tweet_id: str
    ) -> GeneralResponse:
        user_data = verify_user_token(token=token)
        if not user_data["success"]:
            return GeneralResponse(
                msg="Authentication Failed: Token Invalid", success=False
            )
        tweet_obj = tweet_collection.find_one({"_id": ObjectId(tweet_id)})
        if not tweet_obj:
            return GeneralResponse(msg="Tweet Not Found", success=False)
        dislike_obj = likes_collection.update_one(
            {"tweet_id": ObjectId(tweet_id)},
            {"$pull": {"user_id": ObjectId(user_data["response"]["user_id"])}},
        )
        if not dislike_obj.modified_count > 0:
            return GeneralResponse(
                msg="Unable to dislike tweet", success=False
            )
        return GeneralResponse(msg="Disliked Tweet", success=True)
