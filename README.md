# Full Stack Trivia API Backend
The TriviaAPI is a full stack project that has a ready builded React as the front-end. The back-end was builded by me as a challenge to complete the requirments to finish the course on Udacity.
The idea of the project is to enable the users to play trivia question games. They can create their own questions and start quizzes based on a category of quastions.
The Back-end side of the project builded with Python and Flask micro-framework. For this Back-end i have applied the PEP-8 style.

## Getting Started

### Installing Dependencies

To start the TriviaAPI project, you need to have the following tools:
1. Python3 and PIP (Back-end)
2. Node JS & NPM (Front-end)

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### NPM Dependencies

```bash
npm install
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
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

#### Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Introduction

The API builded to make users eable to perform CRUD operations on Trivia game database easily. It have been builded using Flask micro-framework, which is Python framework.
This API was builded for the requirments of graduating of the FSND nanodegree of Udactiy.
All the responses of the API is in JSON format.

### Getting Started

#### Base URL

This project is currently work on localhost, it have not been deployed on a online server.
```
http://127.0.0.1:5000/
```

For the port ```5000``` it's based on your configuration.

### Error

The API have clear and defined errors that will make the debug process easier for developers.

#### Error Types:

- 404 - Not Found
- 400 - Bad Request
- 422 - Unprocesaable

#### Error Response Example:

```
{
    "success": False,
    "error": 404,
    "message": "Resource Not Found"
}
```

### Endpoints Library

This section will contain all the endpoints with their response examples to make everything clear for the users of our API

#### GET /categories

- Return: return list of all the available categories.

- Sample Request: ```curl http://localhost:5000/categories```

- Arguments: None

- Sample Response:
    ```
    {
          "success": True,
          "categories": {
              "1": "Science",
              "2": "Art",
              "3": "History"
          }
    }
    ```
#### GET /questions

- Return: 
    - return list of paginated queations.
    - total of questions available at the server.
    - categories available.
    - the current category.

- Sample Request: ```curl http://localhost:5000/questions?page=1```

- Arguments: 
    - ```page=1```: it will return the page you want with 10 questions per page. [OPTIONAL]

- Sample Response:
    ```
    {
        "success": True,
        "questions": [
            {
              "answer": "Omar ibn al-Khattab", 
              "category": 5, 
              "difficulty": 2, 
              "id": 22, 
              "question": "Who was the bes gladiator in the Arab community?"
            },
            {
              "answer": "30 years", 
              "category": 5, 
              "difficulty": 4, 
              "id": 21, 
              "question": "How many years Muslims lead the world?"
            }
        ],
        "total_questions": 2,
        "categories": {
              "1": "Science",
              "2": "Art",
              "3": "History"
          },
        "current_category": None
    }
    ```

#### DELETE /questions/id

- Return: 
    - return list of paginated queations.
    - the deleted question ID.

- Sample Request: ```curl -X "DELETE" http://localhost:5000/questions/11?page=1```

- Arguments: 
    - ```page=1```: it will return the page you want with 10 questions per page. [OPTIONAL]
    - it take the id of the question in the URL after the ```questions/```

- Sample Response:
    ```
    {
        "success": True,
        "questions": [
            {
              "answer": "Omar ibn al-Khattab", 
              "category": 5, 
              "difficulty": 2, 
              "id": 22, 
              "question": "Who was the bes gladiator in the Arab community?"
            },
            {
              "answer": "30 years", 
              "category": 5, 
              "difficulty": 4, 
              "id": 21, 
              "question": "How many years Muslims lead the world?"
            }
        ],
        "deleted": 11,
    }
    ```

#### POST /questions

- Return: 
    - return list of paginated queations that the you searched for.
    - total of questions available at the server.
    - categories available.
    - the current category.

- Sample Request: 
    ```curl -d '{"searchTerm": "Omar"}' -H "Content-Type: application/json" -X "POST" http://localhost:5000/questions```

- Arguments: 
    - ```searchTerm=Omar```: it will return the questions that contain the keyword. [OPTIONAL]

- Sample Response:
    ```
    {
        "success": True,
        "questions": [
            {
              "answer": "Omar ibn al-Khattab", 
              "category": 5, 
              "difficulty": 2, 
              "id": 22, 
              "question": "Who was the bes gladiator in the Arab community?"
            }
        ],
        "total_questions": 2,
        "categories": {
              "1": "Science",
              "2": "Art",
              "3": "History"
        },
        "current_category": None
    }
    ```

#### POST /questions

- Return: 
    - return list of paginated queations.
    - total of questions available at the server.
    - categories available.
    - the created question.
    - the id of created question.

- Sample Request: 
    ```curl -d '{
        "question": "Who win the elections of 2020 in USA?",
        "answer": "Joe Biden",
        "category": "3",
        "difficulty": 1
        }' 
        -H "Content-Type: application/json" -X "POST" http://localhost:5000/questions```

- Arguments: 
    - ```page=1```: it will return the page you want with 10 questions per page. [OPTIONAL]

- Sample Response:
    ```
    {
        "success": True,
        "questions": [
            {
              "answer": "Omar ibn al-Khattab", 
              "category": 5, 
              "difficulty": 2, 
              "id": 22, 
              "question": "Who was the bes gladiator in the Arab community?"
            },
            {
              "answer": "Donald Trump", 
              "category": 5, 
              "difficulty": 2, 
              "id": 25, 
              "question": "Who is the 45th president of the USA?"
            }
        ],
        "total_questions": 3,
        "created": 25,
        "question_created":             
            {
              "answer": "Donald Trump", 
              "category": 5, 
              "difficulty": 2, 
              "id": 25, 
              "question": "Who is the 45th president of the USA?"
            },
    }
    ```

#### GET /categories/category_id/questions

- Return: 
    - return list of paginated queations of specific category.
    - total of questions available at the server.
    - categories available.
    - the current category.

- Sample Request: ```curl http://localhost:5000/categories/3/questions?page=1```

- Arguments:
    - for this route, the category_id in the URL is [REQUIRED]
    - ```page=1```: it will return the page you want with 10 questions per page. [OPTIONAL]

- Sample Response:
    ```
    {
        "success": True,
        "questions": [
            {
              "answer": "Omar ibn al-Khattab", 
              "category": 5, 
              "difficulty": 2, 
              "id": 22, 
              "question": "Who was the bes gladiator in the Arab community?"
            },
            {
              "answer": "30 years", 
              "category": 5, 
              "difficulty": 4, 
              "id": 21, 
              "question": "How many years Muslims lead the world?"
            }
        ],
        "total_questions": 2,
        "current_category": 3
    }
    ```

#### POST /quizzes

- To play quizz in specific category.

- Return: 
    - return a single random question.

- Sample Request: ```curl http://localhost:5000/quizzes```

- Arguments: None

- Sample Response:
    ```
    {
        "success": True,
        "question": {
            "answer": "Omar ibn al-Khattab", 
            "category": 5, 
            "difficulty": 2, 
            "id": 22, 
            "question": "Who was the bes gladiator in the Arab community?"
        }
    }
    ```

## Authors

Ahmed Asiri authored the API endpoints at the (__init__.py) file, the unittest at the (test_flaskr.py), and the README.md file.
All the other files, folders have been created by Udacity as a project template for the [Full Stack Web Developer Nanodegree](https://classroom.udacity.com/nanodegrees/nd0044-ent/syllabus/core-curriculum).