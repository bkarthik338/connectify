import pytest

from .common.user_common import create_test_user
from .common.user_common import delete_test_user
from .common.user_common import generate_jwt_token_test
from .common.user_common import get_test_user
from .common.user_common import login_test_user
from .common.user_common import reset_password_test_user
from .common.user_common import update_test_user
from models.user_model import GeneralResponse
from models.user_model import GetUserFailureResponse
from models.user_model import GetUserResponse
from models.user_model import LoginResponse


loggedinusertoken = None
loggedinuserobjectid = None


def test_createuser():
    """
    This testcase is to check create user api
    """
    response = create_test_user("createTestUserValid")
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg == "User created Successfully: testuser"


def test_createuseralreadyexist():
    """
    This testcase is to check create user api
    for user which already exists
    """
    response = create_test_user("createTestAlreadyExists")
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Username Already Exists")


def test_createuserinvalidusername():
    """
    This testcase is to check regex fail in create user api
    The Username should have 3-20 characters
    """
    response = create_test_user("createTestUserInvalidUsername")
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Invalid Username")


def test_createuserinvalidemail():
    """
    This testcase is to check regex fail in create user api
    The Email should have valid format
    :user!@example.com (Should not contain !)
    """
    response = create_test_user("createTestUserInvalidEmail")
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Invalid Email")


def test_loginuservalid():
    """
    This testcase is to check the login api where parameters
    are valid username and password
    """
    global loggedinusertoken
    response = login_test_user("loginTestUserValid")
    assert isinstance(response, LoginResponse)
    assert response.success
    assert response.msg.startswith("Login Successful")
    loggedinusertoken = response.token


def test_getuser():
    """
    This testcase is to check get user api
    """
    global loggedinuserobjectid
    response = get_test_user(loggedinusertoken)
    assert isinstance(response, GetUserResponse)
    assert response.success
    assert response.data.username == "testuser"
    loggedinuserobjectid = response.data.id


def test_loginuserinvalidusername():
    """
    This testcase is to check the login api where parameters
    are Invalid username and password (Not registered)
    """
    response = login_test_user("loginTestUserInvalidUsername")
    assert isinstance(response, LoginResponse)
    assert not response.success
    assert response.msg.startswith("Login Failure Invalid Username")


def test_loginuserpasswordmismatch():
    """
    This testcase is to check the login api where parameters
    are Invalid username and password (Not registered)
    """
    response = login_test_user("loginTestUserPasswordMismatch")
    assert isinstance(response, LoginResponse)
    assert not response.success
    assert response.msg.startswith("Incorrect Password")


def test_getuserexpiredtoken():
    """
    This testcase is to check get user api
    which doesn't exist
    """
    global loggedinuserobjectid
    token = generate_jwt_token_test(
        user_id=loggedinuserobjectid, exp_time=True
    )
    response = get_test_user(token=token)
    assert isinstance(response, GetUserFailureResponse)
    assert not response.success
    assert response.error.startswith("Token has expired")


def test_getuserinvalidtoken():
    """
    This testcase is to check get user api
    which doesn't exist
    """
    response = get_test_user(token="12345")
    assert isinstance(response, GetUserFailureResponse)
    assert not response.success
    assert response.error.startswith("Invalid Token")


def test_updateuserdetails():
    """
    This testcase is to check update user api
    using valid data
    """
    global loggedinusertoken
    response = update_test_user("updateTestUserValid", token=loggedinusertoken)
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg == "Updated User Successfully"


def test_updateusersamedetails():
    """
    This testcase is to check update user api
    the data to be updated is same as in the database
    """
    global loggedinusertoken
    response = update_test_user(
        "updateTestUserSameData", token=loggedinusertoken
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "User Updation Failed"


def test_updateuserinvaliddetails():
    """
    This testcase is to check update user api
    where details are invalid like when it has
    only Username and Password
    """
    global loggedinusertoken
    response = update_test_user(
        "updateTestUserInvalid", token=loggedinusertoken
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Invalid data sent for updation"


def test_updateuserinvalidtoken():
    """
    This testcase is to check update user api
    where token sent is invalid
    """
    response = update_test_user("updateTestUserInvalid", token="token")
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Invalid Token"


def test_updateuserexpiredtoken():
    """
    This testcase is to check update user api
    where token sent is invalid
    """
    token = generate_jwt_token_test(
        user_id=loggedinuserobjectid, exp_time=True
    )
    response = update_test_user("updateTestUserInvalid", token=token)
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Token has expired"


def test_resetpasswordsame():
    """
    This testcase is to check reset password api
    where old and new password's are same
    """
    global loggedinusertoken
    response = reset_password_test_user(
        "resetPasswordTestUserSame", token=loggedinusertoken
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "New Password Should Not Be Same As Old Password"


def test_resetpasswordinvalidtoken():
    """
    This testcase is to check reset password api
    where token is invalid
    """
    response = reset_password_test_user(
        "resetPasswordTestUservalid", token="token"
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Invalid Token"


def test_resetpasswordinvalidoldpassword():
    """
    This testcase is to check reset password api
    where old password is incorrect
    """
    global loggedinusertoken
    response = reset_password_test_user(
        "resetPasswordTestUserInvalidOldPassword", token=loggedinusertoken
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Old Password Entered Is Incorrect"


def test_resetpasswordvalid():
    """
    This testcase is to check reset password api
    where all the details are valid
    """
    global loggedinusertoken
    response = reset_password_test_user(
        "resetPasswordTestUservalid", token=loggedinusertoken
    )
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg == "Successfully Updated Password"


def test_deleteuser():
    """
    This testcase is to check delete user api
    """
    response = delete_test_user("deleteTestUser")
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg == "User is deleted."


def test_deleteuserdontexist():
    """
    This testcase is to check delete user api
    which doesn't exists
    """
    response = delete_test_user("deleteTestUserDontExists")
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "User is not registered to delete."


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
