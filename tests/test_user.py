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
    response = create_test_user("createTestUserValid")
    assert isinstance(response, CreateUserResponse)
    assert response.success
    assert response.msg == "User created Successfully: testuser"


def test_createuseralreadyexist():
    """
    This testcase is to check create user api
    for user which already exists
    """
    response = create_test_user("createTestAlreadyExists")
    assert isinstance(response, CreateUserResponse)
    assert not response.success
    assert response.msg.startswith("Username Already Exists")


def test_createuserinvalidusername():
    """
    This testcase is to check regex fail in create user api
    The Username should have 3-20 characters
    """
    response = create_test_user("createTestUserInvalidUsername")
    assert isinstance(response, CreateUserResponse)
    assert not response.success
    assert response.msg.startswith("Invalid Username")


def test_createuserinvalidemail():
    """
    This testcase is to check regex fail in create user api
    The Email should have valid format
    :user!@example.com (Should not contain !)
    """
    response = create_test_user("createTestUserInvalidEmail")
    assert isinstance(response, CreateUserResponse)
    assert not response.success
    assert response.msg.startswith("Invalid Email")


def test_getuser():
    """
    This testcase is to check get user api
    """
    response = get_test_user()
    assert isinstance(response, GetUserResponse)
    assert response.success
    assert response.data.username == "testuser"


def test_deleteuser():
    """
    This testcase is to check delete user api
    """
    response = delete_test_user("deleteTestUser")
    assert isinstance(response, DeleteUserResponse)
    assert response.success
    assert response.msg == "User is deleted."


def test_deleteuserdontexist():
    """
    This testcase is to check delete user api
    which doesn't exists
    """
    response = delete_test_user("deleteTestUserDontExists")
    assert isinstance(response, DeleteUserResponse)
    assert not response.success
    assert response.msg == "User is not registered to delete."


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
