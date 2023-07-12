import strawberry
from bson import ObjectId

from database import db
from models.user_model import GeneralResponse
from utility.user_utility import verify_user_token

tweet_collection = db["tweet"]


@strawberry.type
class TweetMutation:
    @strawberry.mutation
    def create_tweet(
        self, info, token: str, description: str, hashtags: str
    ) -> GeneralResponse:
        user_data = verify_user_token(token=token)
        if not user_data["success"]:
            return GeneralResponse(
                msg=f"Authentication Failed: {user_data['response']}",
                success=False,
            )
        tweet_data = {
            "description": description,
            "hashtags": hashtags,
            "user_id": ObjectId(user_data["response"]["user_id"]),
        }
        _ = tweet_collection.insert_one(tweet_data)
        return GeneralResponse(msg="Tweet Posted Successfully", success=True)
