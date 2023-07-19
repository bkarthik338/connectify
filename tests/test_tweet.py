import pytest
from bson import ObjectId

from .common.test_utility import tweetTestDataJson
from .common.test_utility import userTestDataJson
from models.tweet_model import ListTweetModel
from models.tweet_model import SingleTweetModel
from models.tweet_model import UpdateTweetInput
from models.user_model import GeneralResponse
from models.user_model import LoginResponse
from mutation.tweet_mutation import TweetMutation
from mutation.user_mutation import UserMutation
from query.tweet_query import TweetQuery
from query.user_query import UserQuery

loggedinusertoken = None
tweet_id = None

tweetMutationInstance = TweetMutation()
tweetQueryInstance = TweetQuery()
userMutationInstance = UserMutation()
userQueryInstance = UserQuery()


Info = None


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    global loggedinusertoken
    # Create Test User For Testing Tweet Functionalities
    data = userTestDataJson["createTestUserValid"]
    response = userMutationInstance.create_user(
        Info,
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    assert isinstance(response, GeneralResponse)
    assert response.success, "Creating Test User Failed In The Setup Function"
    assert response.msg == "User created Successfully: testuser"

    # Login And Get The Token
    data = userTestDataJson["loginTestUserValid"]
    response = userQueryInstance.userlogin(
        Info,
        username=data["username"],
        password=data["password"],
        exp_time=None,
    )
    assert isinstance(response, LoginResponse)
    assert response.success, "Unable To Capture Token For Tweet Module Testing"
    assert response.msg.startswith("Login Successful")
    loggedinusertoken = response.token

    yield
    # Teardown code - run once after all the test cases in any file

    data = userTestDataJson["deleteTestUser"]
    response = userMutationInstance.delete_user(
        Info, username=data["username"]
    )
    assert isinstance(response, GeneralResponse)
    assert response.success, "Unable To Delete Created Test User"
    assert response.msg == "User is deleted."


def test_createtweetpost():
    """
    This test is to check the Create Post API
    valid data
    """
    data = tweetTestDataJson["createPostValid"]
    response = tweetMutationInstance.create_tweet(
        Info,
        token=loggedinusertoken,
        description=data["description"],
        # hashtags=data["hashtags"]
    )
    assert isinstance(response, GeneralResponse)
    assert response.success, "Unable To Create New Tweet Post"
    assert response.msg == "Tweet Posted Successfully"


def test_createtweetpostinvalidtoken():
    """
    This test is to check the Create Post API
    with invalid token
    """
    data = tweetTestDataJson["createPostValid"]
    response = tweetMutationInstance.create_tweet(
        Info,
        token="token",
        description=data["description"],
        # hashtags=data["hashtags"]
    )
    assert isinstance(response, GeneralResponse)
    assert (
        not response.success
    ), "Create Post Should Have Failed Sent Invalid Token"
    assert response.msg.startswith("Authentication Failed:")


def test_getallmytweets():
    """
    This test is to check the get all tweets API
    with valid token
    """
    global tweet_id
    test_createtweetpost()
    response = tweetQueryInstance.my_tweets(Info, token=loggedinusertoken)
    assert isinstance(response, ListTweetModel)
    assert response.success
    assert len(response.tweets) > 0
    tweet_id = response.tweets[0].id


def test_getallmytweetsinvalidtoken():
    """
    This test is to check the get all tweets API
    with invalid token
    """
    response = tweetQueryInstance.my_tweets(Info, token="token")
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Authentication Failed")


def test_getsingletweetvalid():
    """
    This test is to check the get Single API using
    Object ID
    """
    global tweet_id
    response = tweetQueryInstance.get_single_tweet(
        Info, token=loggedinusertoken, tweetId=ObjectId(tweet_id)
    )
    assert isinstance(response, SingleTweetModel)
    assert response.success
    assert response.tweet


def test_getsingletweetinvalidtoken():
    """
    This test is to check the get Single API
    where token is invalid
    """
    global tweet_id
    response = tweetQueryInstance.get_single_tweet(
        Info, token="token", tweetId=ObjectId(tweet_id)
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Authentication Failed")


def test_updatetweetvalid():
    """
    This test is to check the Update Tweet API using
    valid data
    """
    global tweet_id
    test_data = tweetTestDataJson["updateTweetValid"]
    tweetModelInstance = UpdateTweetInput().from_dict(test_data)
    response = tweetMutationInstance.update_tweet(
        Info,
        token=loggedinusertoken,
        tweetId=tweet_id,
        updateData=tweetModelInstance,
    )
    assert isinstance(response, SingleTweetModel)
    assert response.success
    assert response.tweet.description.startswith("Updated Description")


def test_updatetweetsamedata():
    """
    This test is to check the Update Tweet API using
    same data, will return error
    """
    global tweet_id
    test_data = tweetTestDataJson["updateTweetValid"]
    tweetModelInstance = UpdateTweetInput().from_dict(test_data)
    response = tweetMutationInstance.update_tweet(
        Info,
        token=loggedinusertoken,
        tweetId=tweet_id,
        updateData=tweetModelInstance,
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Update Tweet Failed")


def test_updatetweetinvalidtoken():
    """
    This test is to check the Update Tweet API using
    invalid token
    """
    global tweet_id
    test_data = tweetTestDataJson["updateTweetValid"]
    tweetModelInstance = UpdateTweetInput().from_dict(test_data)
    response = tweetMutationInstance.update_tweet(
        Info, token="token", tweetId=tweet_id, updateData=tweetModelInstance
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Authentication Failed")


def test_updatetweetoneparameter():
    """
    This test is to check the Update Tweet API using
    one parameter and other parameter won't be changed
    """
    global tweet_id
    test_data = tweetTestDataJson["updateTweetDescription"]
    tweetModelInstance = UpdateTweetInput().from_dict(test_data)
    response = tweetMutationInstance.update_tweet(
        Info,
        token=loggedinusertoken,
        tweetId=tweet_id,
        updateData=tweetModelInstance,
    )
    assert isinstance(response, SingleTweetModel)
    assert response.success
    assert response.tweet.description == "Updated Description Twice"
    assert response.tweet.hashtags == "#UpdatedHashtags"


def test_updatetweetinvaliddata():
    """
    This test is to check the Update Tweet API using
    invalid data
    """
    global tweet_id
    test_data = tweetTestDataJson["updateTweetInvalidData"]
    tweetModelInstance = UpdateTweetInput().from_dict(test_data)
    response = tweetMutationInstance.update_tweet(
        Info,
        token=loggedinusertoken,
        tweetId=tweet_id,
        updateData=tweetModelInstance,
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Invalid Data Sent For Updation"


def test_deletesingletweetvaliddata():
    """
    This test is to check the delete single tweet
    API using valid tweet ID
    """
    global tweet_id
    response = tweetMutationInstance.delete_single_tweet(
        Info, token=loggedinusertoken, tweet_id=tweet_id
    )
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg == "Deleted Tweet"


def test_getsingletweetinvalid():
    """
    This test is to check the get Single API using
    using deleted tweet ID
    """
    global tweet_id
    response = tweetQueryInstance.get_single_tweet(
        Info, token=loggedinusertoken, tweetId=tweet_id
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Tweet Not Found"


def test_deletesingletweetinvalidtoken():
    """
    This test is to check the delete single tweet
    API using invalid token
    """
    global tweet_id
    response = tweetMutationInstance.delete_single_tweet(
        Info, token="token", tweet_id=tweet_id
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Authentication Failed: Invalid Token")


def test_deletesingletweetinvalidtweetid():
    """
    This test is to check the delete single tweet
    API using invalid tweet id
    """
    global tweet_id
    response = tweetMutationInstance.delete_single_tweet(
        Info, token=loggedinusertoken, tweet_id=tweet_id
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Delete Tweet Failed")


def test_deletealltweetvalidtoken():
    """
    This test is to check the delete all user tweet
    API using valid token
    """
    response = tweetMutationInstance.delete_all_tweets(
        Info, token=loggedinusertoken
    )
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg.startswith("Deleted All User Tweets")


def test_deletealltweetinvalidtoken():
    """
    This test is to check the delete all user tweet
    API using invalid token
    """
    response = tweetMutationInstance.delete_all_tweets(Info, token="token")
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Authentication Failed: Invalid Token")


def test_deletealltweetinvalid():
    """
    This test is to check the delete all user tweet
    API with no existing tweets in database
    """
    response = tweetMutationInstance.delete_all_tweets(
        Info, token=loggedinusertoken
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Delete Tweets Failed")


if __name__ == "__main__":
    pytest.main([__file__])
