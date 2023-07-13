from typing import Union

import strawberry
from bson import ObjectId

from constants import TWEET_UPDATE_TABLE_KEYS
from database import db
from models.tweet_model import SingleTweetModel
from models.tweet_model import TweetModel
from models.tweet_model import UpdateTweetInput
from models.user_model import GeneralResponse
from utility.user_utility import verify_user_token

tweet_collection = db["tweet"]


@strawberry.type
class TweetMutation:
    @strawberry.mutation
    def create_tweet(
        self, info, token: str, description: str, hashtags: str = None
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

    @strawberry.mutation
    def update_tweet(
        self, info, token: str, tweetId: str, updateData: UpdateTweetInput
    ) -> Union[GeneralResponse, SingleTweetModel]:
        user_data = verify_user_token(token=token)
        if not user_data["success"]:
            return GeneralResponse(
                msg=f"Authentication Failed: {user_data['response']}",
                success=False,
            )
        data = {}
        update_data = updateData.to_dict()
        for key, value in update_data.items():
            if (key in TWEET_UPDATE_TABLE_KEYS) and (
                value is not None and value != ""
            ):
                data[key] = value
        if not data:
            return GeneralResponse(
                msg="Invalid Data Sent For Updation", success=False
            )
        query = {
            "user_id": ObjectId(user_data["response"]["user_id"]),
            "_id": ObjectId(tweetId),
        }
        updated_obj = tweet_collection.update_one(query, {"$set": data})
        if not updated_obj.modified_count > 0:
            return GeneralResponse(msg="Update Tweet Failed", success=False)
        get_tweet_obj = tweet_collection.find_one(query)
        return SingleTweetModel(
            tweet=TweetModel(
                id=tweetId,
                description=get_tweet_obj["description"],
                hashtags=get_tweet_obj["hashtags"],
            ),
            success=True,
        )
