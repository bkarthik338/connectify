import pytest

from .common.user_common import create_test_user
from .common.user_common import delete_test_user
from .common.user_common import get_test_user
from mutation.user_mutation import CreateUserResponse
from mutation.user_mutation import DeleteUserResponse
from query.user_query import GetUserResponse


def test_createuser():
    """
    This testcase is to check create user api
    """
    response = create_test_user()
    assert isinstance(response, CreateUserResponse)
    assert response.success
    assert response.msg == "User created Successfully: testuser"


def test_getuser():
    """
    This testcase is to check get user api
    """
    response = get_test_user()
    assert isinstance(response, GetUserResponse)
    assert response.success and response.data.username == "testuser"


def test_deleteuser():
    """
    This testcase is to check delete user api
    """
    response = delete_test_user()
    assert isinstance(response, DeleteUserResponse)
    assert response.success and response.msg == "User is deleted."


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
