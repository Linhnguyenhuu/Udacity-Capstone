# Capstone Project

# Instruction
Imagine you are in a company that specializes in recruiting and training actors. And your daily job is to manage the actors of your company and the list available movies that the company plans for them. This project will help you to manage all of that.

Now, follow the instructions below to start up and complete the project.

## How to Run the Backend
#### Step 1 - Start Postgres and set up the database and testing database

Open your postgres sql and create a new database named capstone.
Navigate to backend folder then run:

        . flask db init
        . flask db migrate -m "Initial migration."
        . flask db upgrade

*Note: You can use available query to insert to movie and actor table:

        insert into movies values (1, 'Snow White and the Seven Dwarfs', '1937-01-01 00:00:00');
        insert into movies values (2, 'Pinocchio', '1940-01-01 00:00:00');
        insert into movies values (3, 'Fantasia', '1940-01-01 00:00:00');
        insert into movies values (4, 'The Reluctant Dragon', '1941-01-01 00:00:00');
        insert into movies values (5, 'Dumbo', '1941-01-01 00:00:00');
        insert into movies values (6, 'Bambi', '1942-01-01 00:00:00');
        insert into movies values (7, 'Saludos Amigos', '1943-01-01 00:00:00');
        insert into movies values (8, 'Victory Through Air Power', '1943-01-01 00:00:00');
        insert into movies values (9, 'The Three Caballeros', '1945-01-01 00:00:00');
        insert into movies values (10, 'Make Mine Music', '1946-01-01 00:00:00');
        insert into movies values (11, 'Song of the South', '1946-01-01 00:00:00');
        insert into movies values (12, 'Fun and Fancy Free', '1947-01-01 00:00:00');
        insert into movies values (13, 'Melody Time', '1948-01-01 00:00:00');
        insert into movies values (14, 'So Dear to My Heart', '1949-01-01 00:00:00');
        insert into movies values (15, 'The Adventures of Ichabod and Mr. Toad', '1949-01-01 00:00:00');

        insert into actors values (1, 'Oprah Winfrey', 60, 'female');
        insert into actors values (2, 'Lil Nas X', 30, 'male');
        insert into actors values (3, 'Saweetie', 26, 'female');
        insert into actors values (4, 'Quavo', 40, 'male');
        insert into actors values (5, 'David Tennant', 30, 'male');

Then create .env file in root folder to define environment variables, for example:
DATABASE_URL='postgresql://postgres@localhost:5432/postgres'
AUTH0_DOMAIN='abc'
API_AUDIENCE='abc'

#### Step 2 - Install the required packages
Navigate to the backend directory and run `pip install`

```
cd backend
pip3 install -r requirements.txt
```
#### Step 3. Start the backend server
If you are using MAC, start the (backend) Flask server by running:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Else if Windows:

```cmd
$env:FLASK_APP = "api.py"
set FLASK_APP=api.py
flask run --reload
```

Verify with Postman using udacity-capstone.postman_collection.json file in project folder

The server will restart automatically when changes are detected.

#### Step 4. Authentication using AuthO
1. Go to auth0.com and create an account

2. Login, and click Applications -> Create Application 
    -> Create Application name and Choose Regular Web Application

3. In Settings of created Application -> go to Application URIs
    -> Application Login URI: https://127.0.0.1:8080/login
        Allowed Callback URLs: https://127.0.0.1:8080/login-results
        Allowed Logout URLs: https://127.0.0.1:8080/logout

4. Go to APIs -> Create API -> enter API name and indentifier
    -> In Settings tab of created API -> go to RBAC Settings
    -> enable RBAC + add permissions in the Access Token

5. In User Management -> Roles 
    -> Create 3 roles: Casting Assistant, Casting Director, Executive Producer
    -> In tab permissions of Casting Assistant,
        add these permissions: get:actor, get:actors, get:movie, get:movies
    -> Casting Director: get:actor, get:actors, get:movie, get:movies,
        post:actors, patch:actors, delete:actors, patch:movies
    -> Executive Producer: get:actor, get:actors, get:movie, get:movies,
        post:actors, patch:actors, delete:actors, patch:movies,
        post:movies, delete:movies

6. In User Management -> Users -> Create 3 users and assign 3 corresponding roles

7. In Authentication -> Authentication Profile -> Click Try -> Login
*Note: An test application will auto create for testing your application.
        You will need to go to it -> go to advanced settings
        -> grant types -> check the Implicit checkbox

8. In your browser, copy this:
    https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}

    - YOUR_DOMAIN: is the Tenant Name in Settings->General
    - API_IDENTIFIER: replace by your API Identifier
    - YOUR_CLIENT_ID: go to your Application and copy the Client ID
    - YOUR_CALLBACK_URI: https://127.0.0.1:8080/login-results

9. After step 8, you will see a call back url in your browser look like:
https://127.0.0.1:8080/login-results#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRqQnBkb3BqMzJMRkRVZExPa180MiJ9.eyJpc3MiOiJodHRwczovL2Rldi11Y2pqZWszOGl1YzBmeHMzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzY5NjNjZTgwMGViYzczZWQ0ZDczNjgiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTIyMjM3NSwiZXhwIjoxNzM1MzA4Nzc1LCJzY29wZSI6IiIsImF6cCI6IjlRMTROUEtUeUlIUDFIbThFVVRlT1pwb2NFUHpjSEdRIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.D03TpLJr4O6W1IJZGLF25iKFFUSSqFCQHYCMCPdxtYNCdqLN2ELKshoTCH0LkobicwwQSv932XZSbg6DQny4EKs2D4FgTJlXoqb6-Bmi9pvfaRcGPuLP74s9wNMfZLAJ6ItJqr2nYFtAOVZ7q0SpidbP5w3EW-lypZSbLmuEC9pv7xHkF5w8HatoU1W1zss0Wss9g8J4tjfTDb__VPVX05dEJy2FASb1ekxbnOuAkM-6YuwsLWMBOX8BVuBuZXAnvfLR6IFhRBt1ZLnBpiUBQy4bQOiAPLq8xVaTzjf4uF7jH-KbPuipLAYHbOiDXdHettGsZMJ47asB7kHroxC2zw&expires_in=86400&token_type=Bearer

-> save this token for authentication: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlRqQnBkb3BqMzJMRkRVZExPa180MiJ9.eyJpc3MiOiJodHRwczovL2Rldi11Y2pqZWszOGl1YzBmeHMzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzY5NjNjZTgwMGViYzczZWQ0ZDczNjgiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTczNTIyMjM3NSwiZXhwIjoxNzM1MzA4Nzc1LCJzY29wZSI6IiIsImF6cCI6IjlRMTROUEtUeUlIUDFIbThFVVRlT1pwb2NFUHpjSEdRIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.D03TpLJr4O6W1IJZGLF25iKFFUSSqFCQHYCMCPdxtYNCdqLN2ELKshoTCH0LkobicwwQSv932XZSbg6DQny4EKs2D4FgTJlXoqb6-Bmi9pvfaRcGPuLP74s9wNMfZLAJ6ItJqr2nYFtAOVZ7q0SpidbP5w3EW-lypZSbLmuEC9pv7xHkF5w8HatoU1W1zss0Wss9g8J4tjfTDb__VPVX05dEJy2FASb1ekxbnOuAkM-6YuwsLWMBOX8BVuBuZXAnvfLR6IFhRBt1ZLnBpiUBQy4bQOiAPLq8xVaTzjf4uF7jH-KbPuipLAYHbOiDXdHettGsZMJ47asB7kHroxC2zw


# Completing the Project

## Setting Up Testing

1. Write a test for specific application behavior.
2. Run the test and watch it fail.
3. Write code to execute the required behavior.
4. Test the code and rewrite as necessary to pass the test
5. Refactor your code.
6. Repeat - write your next test.

For this project you need to write at least one test for the success and at least one error behavior of each endpoint using the unittest library. You should write the tests in `backend/test.py`.

The authentication tokens are defined in auth_config.json file. If it expired, you can get the new one and replace it.

To deploy the tests, navigate to the `backend ` directory and run the test file: 

```
cd backend
python test.py
```

## Documenting your Endpoints

Documenting your endpoints is critical so that other users understand how to use the API.  

For this project, you will need to provide detailed documentation of your API endpoints in your project's README.md file.  The documentation for each API endpoint must include:

* URL
* request parameters
* response body. 

Use the example below as a reference.

### Endpoint Documentation

1. `GET '/movies'`

* Fetches a dictionary of movies in which the keys are the ids and the value is the corresponding string of the movies
* Request Arguments: None
* Returns: An object with `movies` and `success`

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "1943-01-01 00:00:00",
            "title": "Victory Through Air Power"
        },
        {
            "id": 2,
            "release_date": "1940-01-01 00:00:00",
            "title": "Pinocchio"
        }
    ],
    "success": true
}
```

2. `GET '/movies/id'`

* Fetches a json of a movie
* Request Arguments: `id` - integer
* Returns: A json include "id", "release_date", "success", "title"

```json
{ 
    "id": 2,
    "release_date": "1940-01-01 00:00:00",
    "success": true,
    "title": "Pinocchio"
}
```

3. `POST '/movies'`

- Sends a post request in order to create a new movie
- Request Body:

```json
{
    "release_date": "1942-01-01 00:00:00",
    "title": "Bambi"
}
```

- Returns: a json including created movie id, and status

```json
{
    "created": 1,
    "success": true
}
```

4. `POST '/movies/search'`

- Sends a post request in order to search for movies
- Request Body:

```json
{
    "searchTerm": "Pinocchio"
}
```

- Returns: An object with `movies` and `success`

```json
{
    "movies": [
        {
            "id": 2,
            "release_date": "1940-01-01 00:00:00",
            "title": "Pinocchio"
        }
    ],
    "success": true
}
```

5. `PATCH '/movies/id'`

- Sends a patch request in order to update a movie
- Request Arguments: `id` - integer
- Request Body:

```json
{
    "release_date": "1937-01-01 00:00:00",
    "title": "Snow White and the Seven Dwarfs"
}
```

- Returns: a json including updated movie id, and status

```json
{
    "success": true,
    "updated": 2
}
```

6. `DELETE 'movies/id'`

- Deletes a specified movie using the id of the movie
- Request Arguments: `id` - integer
- Returns: a json including deleted movie id, and status

```json
{
    "deleted": 2,
    "success": true
}
```

7. `GET '/actors'`

* Fetches a dictionary of actors in which the keys are the ids and the value is the corresponding string of the actors
* Request Arguments: None
* Returns: An object with `actors` and `success`

```json
{
    "actors": [
        {
            "age": 60,
            "gender": "female",
            "id": 1,
            "name": "Oprah Winfrey"
        },
        {
            "age": 21,
            "gender": "male",
            "id": 4,
            "name": "21 Savage"
        }
    ],
    "success": true
}
```

8. `GET '/actors/id'`

* Fetches a json of an actor
* Request Arguments: `id` - integer
* Returns: A json include "id", "age", "success", "gender", "name"

```json
{ 
    "age": 60,
    "gender": "female",
    "id": 1,
    "name": "Oprah Winfrey",
    "success": true
}
```

9. `POST '/actors'`

- Sends a post request in order to create a new actor
- Request Body:

```json
{
    "name": "David Tennant",
    "age": 30,
    "gender": "male"
}
```

- Returns: a json including created actor id, and status

```json
{
    "created": 1,
    "success": true
}
```

10. `POST '/actors/search'`

- Sends a post request in order to search for actors
- Request Body:

```json
{
    "searchTerm": "Oprah Winfrey"
}
```

- Returns: An object with `actors` and `success`

```json
{
    "actors": [
        {
            "age": 60,
            "gender": "female",
            "id": 1,
            "name": "Oprah Winfrey"
        }
    ],
    "success": true
}
```

11. `PATCH '/actors/id'`

- Sends a patch request in order to update an actor
- Request Arguments: `id` - integer
- Request Body:

```json
{
    "name": "21 Savage",
    "age": "27",
    "gender": "male"
}
```

- Returns: a json including updated actor id, and status

```json
{
    "success": true,
    "updated": 2
}
```

12. `DELETE 'actors/id'`

- Deletes a specified actor using the id of the actor
- Request Arguments: `id` - integer
- Returns: a json including deleted actor id, and status

```json
{
    "deleted": 1,
    "success": true
}
```


# Deploy app to Render

## Change the way create db for the most convenience deployment
In models.py file, go to setup_db() and comment out this line:
    migrate = Migrate(app, db)
Then use db.create_all() instead for the most convenience. 

## Deploy app to Render
1. Go to Render.com, create an account and login
2. In the dashboard, create a new PostgreSQL
    -> enter name, and at Plan Options, choose Free -> create database
3. In the dashboard, create a new Web Service
    -> connect to your git repos
    -> enter a name
    -> Build Command: pip install -r requirements.txt
    -> Start Command: gunicorn api:app
    -> Instance Type: Free
    -> Environment Variables: 
        API_AUDIENCE: your API Identifier
        AUTH0_DOMAIN: your application domain
        DATABASE_URL: your db connection string (ex: postgresql://postgres@localhost:5432/postgres)
        PYTHON_VERSION: 3.10.8
    -> create

4. After deployment, use udacity-capstone.postman_collection.json file in project folder to test with Postman
OnRender URL: https://udacity-capstone-gkmb.onrender.com
- you will need to add host environment with this value: https://udacity-capstone-gkmb.onrender.com
- click Casting Assistant -> authorization
    -> choose auth type is Bearer Token
    -> copy the token that match the role Casting Assistant you saved before to Token
    -> do the same with Casting Director and Excutive Producer
- Now, ready to test!