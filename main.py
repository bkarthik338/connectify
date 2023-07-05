import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.asgi import GraphQL

from mutation.mutation import UserMutation
from query.user_query import UserQuery

app = FastAPI()


# Mutation Class which imports all the functionalities Mutation Classes
class Mutation(UserMutation):
    pass


# Query Class which imports all the functionalities Query Classes
class Query(UserQuery):
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
