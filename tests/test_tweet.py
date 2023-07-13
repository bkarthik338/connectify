import pytest

from .common.tweet_common import create_post_test
from .common.tweet_common import get_all_tweets
from .common.tweet_common import get_single_tweet
from .common.tweet_common import update_tweet_test
from .common.user_common import create_test_user
from .common.user_common import delete_test_user
from .common.user_common import login_test_user
from models.tweet_model import ListTweetModel
from models.tweet_model import SingleTweetModel
from models.user_model import GeneralResponse
from models.user_model import LoginResponse

loggedinusertoken = None
tweet_id = None


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    global loggedinusertoken
    # Create Test User For Testing Tweet Functionalities
    response = create_test_user("createTestUserValid")
    assert isinstance(response, GeneralResponse)
    assert response.success, "Creating Test User Failed In The Setup Function"
    assert response.msg == "User created Successfully: testuser"

    # Login And Get The Token
    response = login_test_user("loginTestUserValid")
    assert isinstance(response, LoginResponse)
    assert response.success, "Unable To Capture Token For Tweet Module Testing"
    assert response.msg.startswith("Login Successful")
    loggedinusertoken = response.token

    yield
    # Teardown code - run once after all the test cases in any file

    response = delete_test_user("deleteTestUser")
    assert isinstance(response, GeneralResponse)
    assert response.success, "Unable To Delete Created Test User"
    assert response.msg == "User is deleted."


def test_createtweetpost():
    """
    This test is to check the Create Post API
    valid data
    """
    response = create_post_test("createPostValid", token=loggedinusertoken)
    assert isinstance(response, GeneralResponse)
    assert response.success, "Unable To Create New Tweet Post"
    assert response.msg == "Tweet Posted Successfully"


def test_createtweetpostinvalidtoken():
    """
    This test is to check the Create Post API
    with invalid token
    """
    response = create_post_test("createPostValid", token="token")
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
    response = get_all_tweets(token=loggedinusertoken)
    assert isinstance(response, ListTweetModel)
    assert response.success
    assert len(response.tweets) > 0
    tweet_id = response.tweets[0].id


def test_getallmytweetsinvalidtoken():
    """
    This test is to check the get all tweets API
    with invalid token
    """
    response = get_all_tweets(token="token")
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Authentication Failed")


# TODO Tweet Not Found Test Case
def test_getsingletweetvalid():
    """
    This test is to check the get Single API using
    Object ID
    """
    global tweet_id
    response = get_single_tweet(token=loggedinusertoken, tweet_id=tweet_id)
    assert isinstance(response, SingleTweetModel)
    assert response.success
    assert response.tweet


def test_getsingletweetinvalidtoken():
    """
    This test is to check the get Single API
    where token is invalid
    """
    global tweet_id
    response = get_single_tweet(token="token", tweet_id=tweet_id)
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Authentication Failed")


def test_updatetweetvalid():
    """
    This test is to check the Update Tweet API using
    valid data
    """
    global tweet_id
    response = update_tweet_test(
        "updateTweetValid", token=loggedinusertoken, tweet_id=tweet_id
    )
    assert isinstance(response, SingleTweetModel)
    assert response.success
    assert response.tweet.description.startswith("Updated Description")


def test_updatetweetsamedata():
    """
    This test is to check the Update Tweet API using
    same data, will return error
    """
    response = update_tweet_test(
        "updateTweetValid", token=loggedinusertoken, tweet_id=tweet_id
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Update Tweet Failed")


def test_updatetweetinvalidtoken():
    """
    This test is to check the Update Tweet API using
    invalid token
    """
    response = update_tweet_test(
        "updateTweetValid", token="token", tweet_id=tweet_id
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Authentication Failed")


def test_updatetweetoneparameter():
    """
    This test is to check the Update Tweet API using
    one parameter and other parameter won't be changed
    """
    response = update_tweet_test(
        "updateTweetDescription", token=loggedinusertoken, tweet_id=tweet_id
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
    response = update_tweet_test(
        "updateTweetInvalidData", token=loggedinusertoken, tweet_id=tweet_id
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Invalid Data Sent For Updation"


if __name__ == "__main__":
    pytest.main([__file__])
