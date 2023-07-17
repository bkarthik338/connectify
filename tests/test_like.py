# import pytest
# @pytest.fixture(scope="module", autouse=True)
# def setup_teardown():
#     global loggedinusertoken
#     # Create Test User For Testing Tweet Functionalities
#     response = create_test_user("createTestUserValid")
#     assert isinstance(response, GeneralResponse)
#     assert response.success, "Creating Test User Failed In The Setup Function"
#     assert response.msg == "User created Successfully: testuser"
#     # Login And Get The Token
#     response = login_test_user("loginTestUserValid")
#     assert isinstance(response, LoginResponse)
#     assert response.success, "Unable To Capture Token For Tweet Module Testing"
#     assert response.msg.startswith("Login Successful")
#     loggedinusertoken = response.token
#     yield
#     # Teardown code - run once after all the test cases in any file
#     response = delete_test_user("deleteTestUser")
#     assert isinstance(response, GeneralResponse)
#     assert response.success, "Unable To Delete Created Test User"
#     assert response.msg == "User is deleted."
# if __name__ == "__main__":
#     pytest.main([__file__])
