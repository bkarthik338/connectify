import strawberry
from bson import ObjectId


# Tweet/Post Database Model
@strawberry.type
class TweetModel:
    tweet: str
    hashtags: str = None
    user_id: ObjectId
