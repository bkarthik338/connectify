from typing import Union

import strawberry
from bson import ObjectId

from database import db
from models.tweet_model import ListTweetModel
from models.tweet_model import SingleTweetModel
from models.tweet_model import TweetModel
from models.user_model import GeneralResponse
from utility.user_utility import verify_user_token

tweet_collection = db["tweet"]


@strawberry.type
class TweetQuery:
    @strawberry.field
    def my_tweets(
        self, info, token: str
    ) -> Union[GeneralResponse, ListTweetModel]:
        user_data = verify_user_token(token=token)
        if not user_data["success"]:
            return GeneralResponse(
                msg=f"Authentication Failed: {user_data['response']}",
                success=False,
            )
        response = tweet_collection.find(
            {"user_id": ObjectId(user_data["response"]["user_id"])}
        )
        tweets = [
            TweetModel(
                id=tweet["_id"],
                description=tweet["description"],
                hashtags=tweet["hashtags"],
            )
            for tweet in response
        ]
        return ListTweetModel(success=True, tweets=tweets)

    @strawberry.field
    def get_single_tweet(
        self, info, token: str, tweetId: str
    ) -> Union[GeneralResponse, SingleTweetModel]:
        user_data = verify_user_token(token=token)
        if not user_data["success"]:
            return GeneralResponse(
                msg=f"Authentication Failed: {user_data['response']}",
                success=False,
            )
        response = tweet_collection.find_one({"_id": ObjectId(tweetId)})
        if not response:
            return GeneralResponse(msg="Tweet Not Found", success=False)
        response["id"] = response.pop("_id")
        return SingleTweetModel(
            tweet=TweetModel().from_dict(response), success=True
        )
