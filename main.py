import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.asgi import GraphQL

from mutation.tweet_mutation import TweetMutation
from mutation.user_mutation import UserMutation
from query.tweet_query import TweetQuery
from query.user_query import UserQuery

app = FastAPI()


# Mutation Class which imports all the functionalities Mutation Classes
@strawberry.type
class Mutation(UserMutation, TweetMutation):
    pass


# Query Class which imports all the functionalities Query Classes
@strawberry.type
class Query(UserQuery, TweetQuery):
    pass


# Initialize Fastapi application
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create the GraphQL app
graphql_app = GraphQL(schema)

# Add the GraphQL route to the FastAPI application
app.add_route("/graphql", graphql_app)

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
