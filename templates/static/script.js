// script.js

// Function to render tweets on the page
function renderTweets(tweets) {
  window.location.href = "templates/tweets.html";
  var tweetContainer = parent.document.getElementById("tweet-container");
    tweetContainer.innerHTML = ""; // Clear the existing content

  // Check if the query response contains any errors
  if (tweets.errors) {
      console.error("GraphQL query returned errors:", tweets.errors);
      return;
  }

  // Check if the query response contains tweets
  if (tweets.data && tweets.data.myTweets && tweets.data.myTweets.tweets) {
      var tweetsData = tweets.data.myTweets.tweets;

      // Loop through the tweets and create HTML elements to display each tweet
      tweetsData.forEach(function (tweet) {
          var tweetElement = document.createElement("div");
          tweetElement.classList.add("tweet");

          var tweetId = document.createElement("p");
          tweetId.innerText = "Tweet ID: " + tweet.id;
          tweetElement.appendChild(tweetId);

          var tweetDescription = document.createElement("p");
          tweetDescription.innerText = "Description: " + tweet.description;
          tweetElement.appendChild(tweetDescription);

          var tweetHashtags = document.createElement("p");
          tweetHashtags.innerText = "Hashtags: " + tweet.hashtags;
          tweetElement.appendChild(tweetHashtags);

          var likesCount = document.createElement("p");
          likesCount.innerText = "Likes Count: " + tweet.likesCount;
          tweetElement.appendChild(likesCount);

          var likedUsers = document.createElement("p");
          likedUsers.innerText = "Liked Users:";
          tweetElement.appendChild(likedUsers);

          tweet.likedUsers.forEach(function (user) {
              var userElement = document.createElement("p");
              userElement.innerText = "Username: " + user.username + ", ID: " + user.id;
              tweetElement.appendChild(userElement);
          });

          tweetContainer.appendChild(tweetElement);
      });
  }
}

// Function to handle login form submission
function handleLoginFormSubmit(event) {
  event.preventDefault(); // Prevent form submission

  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  // Make an AJAX request to the server to authenticate the user
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/graphql");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          if (response.data.userlogin["success"]) {
              var token = response.data.userlogin["token"];
              console.log(token)
              fetchTweets(token)
          } else {
              console.error("Login failed:", response.msg);
          }
      }
  };
                      var query = `{
                            userlogin(username: "${username}", password: "${password}") {
                                success
                                msg
                                token
                            }
                        }
                    `
  xhr.send(JSON.stringify({query: query}));
}

// Function to fetch tweets using the provided token
function fetchTweets(token) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/graphql");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          renderTweets(response);
      }
  };

  // Replace "{{root_token}}" in the query with the actual token value
  var query = `{
      myTweets(token: "${token}") {
          ... on GeneralResponse {
              success
              msg
          }
          ... on ListTweetModel {
              success
              tweets {
                  id
                  description
                  hashtags
                  likesCount
                  likedUsers {
                      id
                      username
                  }
              }
          }
      }
  }`;

  xhr.send(JSON.stringify({ query: query }));
}

// Attach event listener to the login form submission
document.getElementById("login-form").addEventListener("submit", handleLoginFormSubmit);
