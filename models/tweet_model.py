import dataclasses
from typing import List
from typing import Optional

import strawberry
from bson import ObjectId

from models.user_model import User


@strawberry.type
class CommentUser:
    user_id: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            if isinstance(value, ObjectId):
                setattr(instance, key, str(value))
            setattr(instance, key, value)
        return instance


# Get Tweets Response Model
@strawberry.type
class TweetModel:
    id: Optional[str] = None
    description: Optional[str] = None
    hashtags: Optional[str] = None
    likes_count: int = 0
    liked_users: List[User] = None
    comments_count: int = 0
    comments: List[CommentUser] = None

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            if isinstance(value, ObjectId):
                setattr(instance, key, str(value))
                continue
            elif key == "liked_users":
                setattr(
                    instance, key, [User().from_dict(user) for user in value]
                )
                continue
            elif key == "comments":
                setattr(
                    instance,
                    key,
                    [CommentUser().from_dict(user) for user in value],
                )
                continue
            setattr(instance, key, value)
        return instance


# SingleTweetModel
@strawberry.type
class SingleTweetModel:
    tweet: TweetModel
    success: bool

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            if isinstance(value, ObjectId):
                setattr(instance, key, value)
                continue
            setattr(instance, key, value)
        return instance


# List of Tweets
@strawberry.type
class ListTweetModel:
    success: bool
    tweets: List[TweetModel]


# UpdateTweetInput
@strawberry.input
class UpdateTweetInput:
    description: Optional[str] = None
    hashtags: Optional[str] = None

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        for key, value in data.items():
            if isinstance(value, ObjectId):
                setattr(instance, key, value)
                continue
            setattr(instance, key, value)
        return instance
