import pytest
from bson import ObjectId

from .common.test_utility import create_users
from .common.test_utility import delete_users
from .common.test_utility import likeTestDataJson
from constants import TWEETS_NAMES_TESTCASE
from constants import USER_NAMES_TESTCASE
from models.user_model import GeneralResponse
from mutation.comment_mutation import CommentMutattion
from mutation.tweet_mutation import TweetMutation
from query.tweet_query import TweetQuery

tweetMutationInstance = TweetMutation()
tweetQueryInstance = TweetQuery()
commentMutationInstance = CommentMutattion()
Info = None
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


def test_addcommentvaliddata():
    """
    This test is to check the Add Comment API
    using valid token and valid tweetId
    """
    response = commentMutationInstance.add_comment(
        Info,
        token=loggedinusertokendict["user1"],
        tweetId=tweetids[0],
        comment="Adding First Comment",
    )
    assert isinstance(response, GeneralResponse)
    assert response.msg == "Successfully Added Comment"
    getTweet = tweetQueryInstance.get_single_tweet(
        Info, token=loggedinusertokendict["user1"], tweetId=tweetids[0]
    )
    assert getTweet.tweet.comments[0].description == "Adding First Comment"


def test_addcommentinvalidtoken():
    """
    This test is to check the Add Comment API
    using invalid token and valid tweetId
    """
    response = commentMutationInstance.add_comment(
        Info,
        token="token",
        tweetId=tweetids[0],
        comment="Adding First Comment",
    )
    assert isinstance(response, GeneralResponse)
    assert response.msg.startswith("Authentication Failed")


def test_addcommentinvalidtweetId():
    """
    This test is to check the Add Comment API
    using valid token and invalid tweetId
    """
    response = commentMutationInstance.add_comment(
        Info,
        token=loggedinusertokendict["user1"],
        tweetId=ObjectId("000000000000000000000000"),
        comment="Adding First Comment",
    )
    assert isinstance(response, GeneralResponse)
    assert response.msg.startswith("Tweet Not Found")
