import pytest
from bson import ObjectId

from .common.test_utility import create_users
from .common.test_utility import delete_users
from .common.test_utility import likeTestDataJson
from constants import TWEETS_NAMES_TESTCASE
from constants import USER_NAMES_TESTCASE
from models.user_model import GeneralResponse
from mutation.likes_mutation import LikesMutattion
from mutation.tweet_mutation import TweetMutation
from mutation.user_mutation import UserMutation
from query.tweet_query import TweetQuery
from query.user_query import UserQuery

Info = None
userQueryInstance = UserQuery()
userMutationInstance = UserMutation()
tweetMutationInstance = TweetMutation()
likeMutationInstance = LikesMutattion()
tweetQueryInstance = TweetQuery()
loggedinusertokendict = {}
tweetids = []


def create_posts(token: str, tweetNames=[]) -> None:
    for tweet in tweetNames:
        data = likeTestDataJson[tweet]
        response = tweetMutationInstance.create_tweet(
            Info,
            token=token,
            description=data["description"],
            hashtags=data["hashtags"],
        )
        assert isinstance(response, GeneralResponse)
        assert response.success, "Unable To Create New Tweet Post"
        assert response.msg == "Tweet Posted Successfully"


def get_all_mytweets(token: str) -> dict:
    response = tweetQueryInstance.my_tweets(Info, token=token)
    tweetIdList = []
    for tweet in response.tweets:
        tweetIdList.append(str(tweet.id))
    return tweetIdList


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    global tweetids
    global loggedinusertokendict
    # Create Four Users ["rootUser", "user1", "user2", "user3"]
    loggedinusertokendict = create_users(users_list=USER_NAMES_TESTCASE)
    # Create Posts for Root User
    _ = create_posts(loggedinusertokendict["rootUser"], TWEETS_NAMES_TESTCASE)
    tweetids = get_all_mytweets(loggedinusertokendict["rootUser"])
    yield
    # Teardown code - run once after all the test cases in any file
    deleteTweetsResponse = tweetMutationInstance.delete_all_tweets(
        Info, token=loggedinusertokendict["rootUser"]
    )
    deleteTweetsResponse.msg == "Deleted All User Tweets"
    response = delete_users(users_list=USER_NAMES_TESTCASE)
    assert response == "Users Deleted"


def test_likepostvaliddata():
    """
    This test is to check the Like API
    using valid token and valid tweetId
    """
    response = likeMutationInstance.like_tweet(
        Info, token=loggedinusertokendict["user1"], tweet_id=tweetids[0]
    )
    assert isinstance(response, GeneralResponse)
    assert response.msg == "Liked The Tweet"
    getTweet = tweetQueryInstance.get_single_tweet(
        Info, token=loggedinusertokendict["user1"], tweetId=tweetids[0]
    )
    assert getTweet.tweet.likes_count == 1


def test_likepostinvalidtoken():
    """
    This test is to check the Like API
    using invalid token and valid TweetID
    """
    response = likeMutationInstance.like_tweet(
        Info, token="token", tweet_id=tweetids[0]
    )
    assert isinstance(response, GeneralResponse)
    response.msg.startswith("Authentication Failed")


def test_likepostinvalidtweetid():
    """
    This test is to check the Like API
    using valid token and invalid TweetID
    """
    response = likeMutationInstance.like_tweet(
        Info,
        token=loggedinusertokendict["user1"],
        tweet_id=ObjectId("000000000000000000000000"),
    )
    assert isinstance(response, GeneralResponse)
    response.msg.startswith("Tweet Not Found")


def test_dislikepostvalid():
    """
    This test is to check the dislike functionality
    using valid token and tweetID
    """
    response = likeMutationInstance.dislike_tweet(
        Info, token=loggedinusertokendict["user1"], tweet_id=tweetids[0]
    )
    assert isinstance(response, GeneralResponse)
    response.msg = "Disliked Tweet"


def test_dislikepostinvalidtoken():
    """
    This test is to check the dislike functionality
    using invalid token
    """
    response = likeMutationInstance.dislike_tweet(
        Info, token="token", tweet_id=tweetids[0]
    )
    assert isinstance(response, GeneralResponse)
    response.msg.startswith("Authentication Failed")


def test_dislikepostinvalidtweetid():
    """
    This test is to check the dislike functionality
    using invalid token
    """
    response = likeMutationInstance.dislike_tweet(
        Info,
        token=loggedinusertokendict["user1"],
        tweet_id=ObjectId("000000000000000000000000"),
    )
    assert isinstance(response, GeneralResponse)
    response.msg.startswith("Tweet Not Found")


if __name__ == "__main__":
    pytest.main([__file__])
