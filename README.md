Social Media Platform Backend
This repository contains the backend application for a Social Media Platform. The application is built using GraphQL with the Strawberry package and utilizes FastAPI as the server. It also includes test cases and test data. The repository is configured to run automatically on each pull request to the development branch.

Features
GraphQL API: The backend provides a GraphQL API to interact with the Social Media Platform.
Tweet CRUD: Users can create, read, update, and delete tweets.
Comment CRUD: Users can create, read, update, and delete comments on tweets.
Like/Dislike Tweets: Users can like or dislike tweets.
User Management: The application includes CRUD functionality for user management.
Technologies Used
GraphQL: The API is built using GraphQL to provide a flexible and efficient way to interact with the application.
Strawberry: Strawberry is used as the GraphQL library to define the schema and resolvers.
FastAPI: FastAPI is the web framework used to build the server and handle HTTP requests.
Test Cases: The repository includes comprehensive test cases to ensure the application's reliability and correctness.
Test Data: Test data is provided to simulate different scenarios and edge cases during testing.
Setup
To run the application locally, follow these steps:

Clone the repository to your local machine.
Install the required dependencies by running: pip install -r requirements.txt.
Set up the database and ensure it is accessible by the application.
Configure the necessary environment variables (if any) for the application.
Run the application using: python app.py.
Testing
The repository includes a suite of test cases to ensure the application functions as expected. To run the tests, execute the following command:

Copy code
pytest
The tests will cover different scenarios and verify the correctness of the application's behavior.
