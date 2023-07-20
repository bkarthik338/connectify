import json
import os

import pytest
from dotenv import load_dotenv

from .common.test_utility import generate_jwt_token_test
from models.user_model import GeneralResponse
from models.user_model import GetUserFailureResponse
from models.user_model import GetUserResponse
from models.user_model import LoginResponse
from models.user_model import UpdateUserInput
from mutation.user_mutation import UserMutation
from query.user_query import UserQuery


load_dotenv()
Info = None
base_url = os.environ.get("BASE_URL")
current_dir = os.path.dirname(os.path.abspath(__file__))
user_json_file_path = os.path.join(current_dir, "testdata/user_testcases.json")


def load_user_json_file():
    """
    This function is to load use test data json file
    """
    with open(user_json_file_path) as file:
        data = json.load(file)
    return data


userTestDataJson = load_user_json_file()

loggedinusertoken = None
loggedinuserobjectid = None

# Instances for Query and Mutation Classes
userMutationInstance = UserMutation()
userQueryInstance = UserQuery()


def test_createuser():
    """
    This testcase is to check create user api
    """
    data = userTestDataJson["createTestUserValid"]
    response = userMutationInstance.create_user(
        Info,
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg == "User created Successfully: testuser"


def test_createuseralreadyexist():
    """
    This testcase is to check create user api
    for user which already exists
    """
    data = userTestDataJson["createTestAlreadyExists"]
    response = userMutationInstance.create_user(
        Info,
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Username Already Exists")


def test_createuserinvalidusername():
    """
    This testcase is to check regex fail in create user api
    The Username should have 3-20 characters
    """
    data = userTestDataJson["createTestUserInvalidUsername"]
    response = userMutationInstance.create_user(
        Info,
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Invalid Username")


def test_createuserinvalidemail():
    """
    This testcase is to check regex fail in create user api
    The Email should have valid format
    :user!@example.com (Should not contain !)
    """
    data = userTestDataJson["createTestUserInvalidEmail"]
    response = userMutationInstance.create_user(
        Info,
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg.startswith("Invalid Email")


def test_loginuservalid():
    """
    This testcase is to check the login api where parameters
    are valid username and password
    """
    global loggedinusertoken
    data = userTestDataJson["loginTestUserValid"]
    response = userQueryInstance.userlogin(
        Info,
        username=data["username"],
        password=data["password"],
        exp_time=None,
    )
    assert isinstance(response, LoginResponse)
    assert response.success
    assert response.msg.startswith("Login Successful")
    loggedinusertoken = response.token


def test_getuser():
    """
    This testcase is to check get user api
    """
    global loggedinuserobjectid
    response = userQueryInstance.getuser(Info, loggedinusertoken)
    assert isinstance(response, GetUserResponse)
    assert response.success
    assert response.data.username == "testuser"
    loggedinuserobjectid = response.data.id


def test_loginuserinvalidusername():
    """
    This testcase is to check the login api where parameters
    are Invalid username and password (Not registered)
    """
    data = userTestDataJson["loginTestUserInvalidUsername"]
    response = userQueryInstance.userlogin(
        Info,
        username=data["username"],
        password=data["password"],
        exp_time=None,
    )
    assert isinstance(response, LoginResponse)
    assert not response.success
    assert response.msg.startswith("Login Failure Invalid Username")


def test_loginuserpasswordmismatch():
    """
    This testcase is to check the login api where parameters
    are Invalid username and password (Not registered)
    """
    data = userTestDataJson["loginTestUserPasswordMismatch"]
    response = userQueryInstance.userlogin(
        Info,
        username=data["username"],
        password=data["password"],
        exp_time=None,
    )
    assert isinstance(response, LoginResponse)
    assert not response.success
    assert response.msg.startswith("Incorrect Password")


def test_getuserexpiredtoken():
    """
    This testcase is to check get user api
    in which token is already expired
    """
    global loggedinuserobjectid
    token = generate_jwt_token_test(
        user_id=loggedinuserobjectid, exp_time=True
    )
    response = userQueryInstance.getuser(Info, token)
    assert isinstance(response, GetUserFailureResponse)
    assert not response.success
    assert response.error.startswith("Token has expired")


def test_getuserinvalidtoken():
    """
    This testcase is to check get user api
    which doesn't exist
    """
    response = userQueryInstance.getuser(Info, "12345")
    assert isinstance(response, GetUserFailureResponse)
    assert not response.success
    assert response.error.startswith("Invalid Token")


def test_updateuserdetails():
    """
    This testcase is to check update user api
    using valid data
    """
    global loggedinusertoken
    data = userTestDataJson["updateTestUserValid"]
    response = userMutationInstance.update_user(
        Info,
        token=loggedinusertoken,
        user_input=UpdateUserInput.from_json(json.dumps(data)),
    )
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg == "Updated User Successfully"


def test_updateusersamedetails():
    """
    This testcase is to check update user api
    the data to be updated is same as in the database
    """
    global loggedinusertoken
    data = userTestDataJson["updateTestUserSameData"]
    response = userMutationInstance.update_user(
        Info,
        token=loggedinusertoken,
        user_input=UpdateUserInput.from_json(json.dumps(data)),
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
    data = userTestDataJson["updateTestUserInvalid"]
    response = userMutationInstance.update_user(
        Info,
        token=loggedinusertoken,
        user_input=UpdateUserInput.from_json(json.dumps(data)),
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Invalid data sent for updation"


def test_updateuserinvalidtoken():
    """
    This testcase is to check update user api
    where token sent is invalid
    """
    data = userTestDataJson["updateTestUserInvalid"]
    response = userMutationInstance.update_user(
        Info,
        token="token",
        user_input=UpdateUserInput.from_json(json.dumps(data)),
    )
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
    data = userTestDataJson["updateTestUserInvalid"]
    response = userMutationInstance.update_user(
        Info,
        token=token,
        user_input=UpdateUserInput.from_json(json.dumps(data)),
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "Token has expired"


def test_resetpasswordsame():
    """
    This testcase is to check reset password api
    where old and new password's are same
    """
    global loggedinusertoken
    data = userTestDataJson["resetPasswordTestUserSame"]
    response = userMutationInstance.reset_password(
        Info,
        token=loggedinusertoken,
        oldPassword=data["old_password"],
        newPassword=data["new_password"],
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "New Password Should Not Be Same As Old Password"


def test_resetpasswordinvalidtoken():
    """
    This testcase is to check reset password api
    where token is invalid
    """
    data = userTestDataJson["resetPasswordTestUservalid"]
    response = userMutationInstance.reset_password(
        Info,
        token="token",
        oldPassword=data["old_password"],
        newPassword=data["new_password"],
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
    data = userTestDataJson["resetPasswordTestUserInvalidOldPassword"]
    response = userMutationInstance.reset_password(
        Info,
        token=loggedinusertoken,
        oldPassword=data["old_password"],
        newPassword=data["new_password"],
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
    data = userTestDataJson["resetPasswordTestUservalid"]
    response = userMutationInstance.reset_password(
        Info,
        token=loggedinusertoken,
        oldPassword=data["old_password"],
        newPassword=data["new_password"],
    )
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg == "Successfully Updated Password"


def test_deleteuser():
    """
    This testcase is to check delete user api
    """
    data = userTestDataJson["deleteTestUser"]
    response = userMutationInstance.delete_user(
        Info, username=data["username"]
    )
    assert isinstance(response, GeneralResponse)
    assert response.success
    assert response.msg == "User is deleted."


def test_deleteuserdontexist():
    """
    This testcase is to check delete user api
    which doesn't exists
    """
    data = userTestDataJson["deleteTestUserDontExists"]
    response = userMutationInstance.delete_user(
        Info, username=data["username"]
    )
    assert isinstance(response, GeneralResponse)
    assert not response.success
    assert response.msg == "User is not registered to delete."


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
