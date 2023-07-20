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
like_collection = db["like"]
user_collection = db["user"]


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
        pipeline = [
            {
                "$match": {
                    "user_id": ObjectId(user_data["response"]["user_id"])
                }
            },
            {
                "$lookup": {
                    "from": "like",
                    "localField": "_id",
                    "foreignField": "tweet_id",
                    "as": "liked_users",
                },
            },
            {
                "$lookup": {
                    "from": "user",
                    "localField": "liked_users.user_id",
                    "foreignField": "_id",
                    "as": "user_objects",
                }
            },
            {
                "$project": {
                    "id": {"$toString": "$_id"},
                    "_id": 0,
                    "description": 1,
                    "hashtags": 1,
                    "likes_count": {
                        "$size": {
                            "$reduce": {
                                "input": "$user_objects.user_id",
                                "initialValue": [],
                                "in": {"$concatArrays": ["$$value", "$$this"]},
                            }
                        }
                    },
                    "liked_users": {
                        "$map": {
                            "input": "$user_objects",
                            "as": "user",
                            "in": {
                                "username": "$$user.username",
                                "id": {"$toString": "$$user._id"},
                            },
                        }
                    },
                }
            },
        ]
        tweets = list(tweet_collection.aggregate(pipeline))
        response_tweets = [TweetModel().from_dict(tweet) for tweet in tweets]
        return ListTweetModel(success=True, tweets=response_tweets)

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
        pipeline = [
            {"$match": {"_id": ObjectId(tweetId)}},
            {"$limit": 1},
            {
                "$lookup": {
                    "from": "like",
                    "localField": "_id",
                    "foreignField": "tweet_id",
                    "as": "likeDocument",
                },
            },
            {
                "$lookup": {
                    "from": "user",
                    "localField": "likeDocument.user_id",
                    "foreignField": "_id",
                    "as": "user_objects",
                }
            },
            {
                "$project": {
                    "id": {"$toString": "$_id"},
                    "description": 1,
                    "hashtags": 1,
                    "likes_count": {
                        "$size": {
                            "$reduce": {
                                "input": "$likeDocument.user_id",
                                "initialValue": [],
                                "in": {"$concatArrays": ["$$value", "$$this"]},
                            },
                        }
                    },
                    "_id": 0,
                    "liked_users": {
                        "$map": {
                            "input": "$user_objects",
                            "as": "user",
                            "in": {
                                "username": "$$user.username",
                                "id": {"$toString": "$$user._id"},
                            },
                        }
                    },
                }
            },
        ]
        response = next(iter(tweet_collection.aggregate(pipeline)), {})
        if not response:
            return GeneralResponse(msg="Tweet Not Found", success=False)
        return SingleTweetModel(
            tweet=TweetModel().from_dict(response), success=True
        )
