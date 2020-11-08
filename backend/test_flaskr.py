import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres',
            'admin',
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'who win the elections of USA 2020?',
            'answer': 'Joe Paiden',
            'difficulty': 3,
            'category': '3'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    def test_creating_questions_success(self):
        response = self.client().post(
            '/questions', json={
                'question': 'who win the elections of USA 2020?',
                'answer': 'Joe Paiden',
                'difficulty': 3,
                'category': '3'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_creating_questions_failure(self):
        response = self.client().post(
            '/questions', json={
                'question': 'who win the elections of USA 2020?',
                'answer': 'Joe Paiden',
                'difficy': 3,
                'categ': '3'})
        # create POST operation with BAD REQUEST
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_get_paginated_questions_success(self):
        # initiate to get questions with pagination
        response = self.client().get('/questions')
        data = json.loads(response.data)

        # assertion test
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_paginated_questions_failure(self):
        # initiate to get questions with pagination
        response = self.client().get('/questions?page=152')
        data = json.loads(response.data)

        # assertion test
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_categories_success(self):
        # initiate request to get all the categories in the DB
        response = self.client().get('/categories')
        data = json.loads(response.data)

        # assertion test
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

    # def test_get_categories_failure(self):
    #     # initiate request to get all the categories in the DB
    #     response = self.client().get('/categories')
    #     data = json.loads(response.data)

    #     # assertion test
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)

    def test_delete_question_success(self):
        # initiate response delete the first questions stored in the DB
        response = self.client().delete('/questions/{}'.format(Question.query.first().id))
        data = json.loads(response.data)

        # assertion test
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_failure(self):
        # initiate response delete the first questions stored in the DB
        response = self.client().delete('/questions/{}'.format(254))
        data = json.loads(response.data)

        # assertion test
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_search_in_questions_success(self):
        # initiate response to search for questions with
        # the search term of 'win'
        response = self.client().post('/questions', json={
            'searchTerm': 'win'
        })
        data = json.loads(response.data)

        # assertion test
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_in_questions_failure(self):
        # initiate response to search for questions with
        # the search term of 'asdfaksdjfahj'
        response = self.client().post('/questions', json={
            'searchTerm': 'asdfaksdjfahj'
        })
        data = json.loads(response.data)

        # assertion test
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_questions_by_categories_success(self):
        # initiate response of category 3 to get questions
        response = self.client().get('/categories/3/questions')
        data = json.loads(response.data)

        # assertion test
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_questions_by_categories_failure(self):
        # initiate response of category 3 to get questions
        response = self.client().get('/categories/545624/questions')
        data = json.loads(response.data)

        # assertion test
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_play_quiz_success(self):
        '''
        tests playing a quizs
        '''

        # loading response with previous question 
        # as first question, and category of 3
        response = self.client().post('/quizzes', json={
            'previous_questions': [Question.query.first().id],
            'quiz_category': {'id': 3}
        })
        data = json.loads(response.data)
        # assertion test
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz_failure(self):
        '''
        tests playing a quizs
        '''

        # loading response with previous question 
        # as first question, and category of 3
        response = self.client().post('/quizzes', json={
            'previous_questions': [555],
            'quiz_category': {'id': 454}
        })
        data = json.loads(response.data)
        # assertion test
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()
