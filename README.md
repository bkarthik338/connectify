<!DOCTYPE html>
<html>
<head>
    <title>Social Media Platform Backend</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f1f1f1;
            margin: 0;
            padding: 0;
        }

        header {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 20px;
        }

        main {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        img {
            max-width: 100%;
        }

        h1 {
            color: #333;
        }

        p {
            color: #666;
        }

        ul {
            list-style: none;
            padding: 0;
        }

        li {
            padding: 10px 0;
            border-bottom: 1px solid #ccc;
        }

        .technology-stack {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
        }

        .technology-item {
            padding: 10px;
        }

        .technology-image {
            max-width: 100px;
            max-height: 100px;
        }

        .contributing-guidelines {
            margin-top: 20px;
            color: #555;
        }

        .contact-info {
            margin-top: 20px;
            color: #555;
        }

        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Social Media Platform Backend</h1>
    </header>

    <main>
        <img src="images/project-logo.png" alt="Project Logo">

        <h2>Features</h2>
        <ul>
            <li>GraphQL API: The backend provides a GraphQL API to interact with the Social Media Platform.</li>
            <li>Tweet CRUD: Users can create, read, update, and delete tweets.</li>
            <li>Comment CRUD: Users can create, read, update, and delete comments on tweets.</li>
            <li>Like/Dislike Tweets: Users can like or dislike tweets.</li>
            <li>User Management: The application includes CRUD functionality for user management.</li>
        </ul>

        <h2>Technologies Used</h2>
        <div class="technology-stack">
            <div class="technology-item">
                <img class="technology-image" src="images/graphql.png" alt="GraphQL">
                <p>GraphQL</p>
            </div>
            <div class="technology-item">
                <img class="technology-image" src="images/strawberry.png" alt="Strawberry">
                <p>Strawberry</p>
            </div>
            <div class="technology-item">
                <img class="technology-image" src="images/fastapi.png" alt="FastAPI">
                <p>FastAPI</p>
            </div>
            <div class="technology-item">
                <img class="technology-image" src="images/pytest.png" alt="Pytest">
                <p>Test Cases</p>
            </div>
        </div>

        <h2>Setup</h2>
        <p>
            To run the application locally, follow these steps:
            <ol>
                <li>Clone the repository to your local machine.</li>
                <li>Install the required dependencies by running: <code>pip install -r requirements.txt</code>.</li>
                <li>Set up the database and ensure it is accessible by the application.</li>
                <li>Configure the necessary environment variables (if any) for the application.</li>
                <li>Run the application using: <code>python app.py</code>.</li>
            </ol>
        </p>

        <h2>Testing</h2>
        <p>
            The repository includes a suite of test cases to ensure the application functions as expected. To run the tests, execute the following command:
            <br>
            <code>pytest</code>
        </p>

        <h2>Contributing</h2>
        <p class="contributing-guidelines">
            If you'd like to contribute to this project, please follow the guidelines outlined in the CONTRIBUTING.md file. We welcome all contributions and bug reports.
        </p>

        <h2>License</h2>
        <p>
            This project is licensed under the MIT License. Feel free to use, modify, and distribute the code as per the terms of the license.
        </p>

        <h2>Contact</h2>
        <p class="contact-info">
            For any questions or support, please contact: <a href="mailto:your-contact-email@example.com">your-contact-email@example.com</a>
        </p>
    </main>

    <footer>
        &copy; 2023 Your Company. All rights reserved.
    </footer>
</body>
</html>
