from typing import List

import strawberry


# Get Tweets Response Model
@strawberry.type
class TweetModel:
    id: str
    description: str
    hashtags: str = None


@strawberry.type
class ListTweetModel:
    success: bool
    tweets: List[TweetModel]
