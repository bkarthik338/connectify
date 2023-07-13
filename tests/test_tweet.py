import pytest

from .common.tweet_common import create_post_test
from .common.user_common import create_test_user
from .common.user_common import delete_test_user
from .common.user_common import login_test_user
from models.user_model import GeneralResponse
from models.user_model import LoginResponse

loggedinusertoken = None


@pytest.fixture(scope="function", autouse=True)
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

    response = delete_test_user("deleteTestUser")
    assert isinstance(response, GeneralResponse)
    assert response.success, "Unable To Delete Created Test User"
    assert response.msg == "User is deleted."


def test_createtweetpost():
    """
    This test is to check the Create Post API
    valid data
    """
    response = create_post_test("CreatePostValid", token=loggedinusertoken)
    assert isinstance(response, GeneralResponse)
    assert response.success, "Unable To Create New Tweet Post"
    assert response.msg == "Tweet Posted Successfully"


def test_createtweetpostinvalidtoken():
    """
    This test is to check the Create Post API
    with invalid token
    """
    response = create_post_test("CreatePostValid", token="token")
    assert isinstance(response, GeneralResponse)
    assert (
        not response.success
    ), "Create Post Should Have Failed Sent Invalid Token"
    assert response.msg.startswith("Authentication Failed:")


if __name__ == "__main__":
    pytest.main([__file__])
