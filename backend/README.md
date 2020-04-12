# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Database Setup for Testing
With Postgres running, restore a test database using the trivia.psql. From the backend folder in terminal run:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Reference

#### Base URL
At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://localhost:5000/`. which is set as a proxy in the frontend configuration.

#### Authentication
This version of the application does not require authentication or API keys.

#### Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "success": False,
  "error: 400,
  "message": "bad request
}
```
The API will return four error types when requests fail:
* 400: Bad Request
* 404: Resource Not Found
* 405: Method not allowed
* 422: Not Processable

### Endpoints
  * GET '/categories'
    * General
      * Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
      * Request Arguments: None
      * Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

    * Sample: `curl -X GET http://127.0.0.1:5000/categories`
      ```
        {
          "success": true,
          "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
          }
        }
      ```

  * GET '/questions'
    * General
      * Returns a list of questions, total question number, categories, current_category and success value.
      * Results are paginated in groups of 10. Include a request argument to choose a page number, starting from 1.
      * Request Arguments: `?page=1`
      * Returns: A list of questions, total question number, categories, current_category and success value.

    * Sample: `curl -X GET http://127.0.0.1:5000/questions?page=1`
      ```
        {
          "success": true,
          "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
          },
          "current_category": "Entertainment",
          "questions": [
            {
              "answer": "Tom Cruise",
              "category": 5,
              "difficulty": 4,
              "id": 4,
              "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            },{...}
          ],
          "total_questions": 19
        }
      ```

  * DELETE '/questions/<int:question_id>'
    * General
      * Deletes the question that has given
      * Request Arguments: `question_id`
      * Returns: Success value.

    * Sample: `curl -X DELETE http://127.0.0.1:5000/questions/9`
      ```
        {
          "success": true,
        }
      ```

  * POST '/questions'
    * General
      * Posts new question
      * Request Arguments: None
      * Request Body: Must include question(type str), answer(type str), difficulty(type int), category(type int)
      * Returns: Success value.

    * Sample: `curl -d '{"question":"xyz","answer":"xyz", "difficulty": 2, "category": 2}' -H "Content-Type: application/json" -X POST http://localhost:5000/questions`
      ```
        {
          "success": true,
        }
      ```

  * POST '/questions/search'
    * General
      * Posts a search query
      * Request Arguments: None
      * Request Body: Must include searchTerm(type str)
      * Returns: A list of questions, total question count, current category and success value.

    * Sample: `curl -d '{"searchTerm":"title"}' -H "Content-Type: application/json" -X POST http://localhost:5000/questions/search`
      ```
        {
          "success": true,
          "current_category": "History",
          "total_questions": 2,
          "questions": [
            {
              "answer": "Maya Angelou",
              "category": 4,
              "difficulty": 2,
              "id": 5,
              "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {...}
          ]
        }
      ```

  * GET '/categories/<int:category_id>/questions'
    * General
      * Gets a list of questions based on a category
      * Request Arguments: `category_id`
      * Returns: A list of questions, total question count, current category and success value.

    * Sample: `curl -X GET http://localhost:5000/categories/3/questions`
      ```
        {
          "success": true,
          "current_category": "Geography",
          "questions": [
            {
              "answer": "Lake Victoria",
              "category": 3,
              "difficulty": 2,
              "id": 13,
              "question": "What is the largest lake in Africa?"
            },{...}
          ],
          "total_questions": 3
        }
      ```

  * POST '/quizzes'
    * General
      * Gets a random question that is not previously selected.
      * Request Arguments: None.
      & Request Body: Must include previous_questions(type list), quiz_category(type dict)
      * Returns: A random question in dict type and success value.

    * Sample: `curl -d '{"previous_questions":[], "quiz_category": {"id": 1, "type":"Science"}}' -H "Content-Type: application/json" -X POST http://localhost:5000/quizzes`
      ```
        {
          "success": true,
          "question": {{
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
          },
        }
      ```

### Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```