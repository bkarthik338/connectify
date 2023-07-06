import pytest
import requests
from pymongo import MongoClient

from query.user_query import GetUserResponse
from query.user_query import UserQuery

client = MongoClient("mongodb://localhost:27017/")
test_db = client["connectify-testcases-db"]
user_collection = test_db["user"]

BASE_URL = "http://localhost:8000/graphql"


@pytest.fixture(scope="module")
def setup_database():
    # Connect to the test database
    # Insert test data
    user_data = {"username": "testuser", "email": "test@example.com"}
    test_db.user.insert_one(user_data)

    # Provide the test database object
    yield test_db

    # Clean up after the tests by removing the inserted data
    test_db.user.delete_one({"username": "testuser"})


# Test case for the create_user mutation
def test_create_user():
    # Define the mutation query
    mutation = """
        mutation {
            createUser(username: "testuser", email: "test@example.com", password: "password") {
                success
                msg
            }
        }
    """

    # Send the request to the API
    response = requests.post(BASE_URL, json={"query": mutation})

    # Check the response status code
    assert response.status_code == 200

    # Parse the response JSON
    data = response.json()["data"]["createUser"]

    # Check the values in the response
    assert data["success"], "Failed to createUser"
    assert data["msg"] == "User created Successfully: testuser"


def test_getuser(setup_database):
    # Create an instance of the UserQuery class
    user_query = UserQuery()

    # Call the getuser function with a test ID
    result = user_query.getuser(info=None, username="testuser")

    assert isinstance(result, GetUserResponse)

    # Assert that the returned User object has the expected values
    assert result.data.username == "testuser"
    assert result.data.email == "test@example.com"


def test_getuser_not_found(setup_database):
    user_query = UserQuery()
    result = user_query.getuser(info=None)
    assert not result.success, "User was found"


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
