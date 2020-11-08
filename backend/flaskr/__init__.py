import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagination(request, questions_list):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in
                           questions_list[start:end]]
    return formatted_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
        )
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():

        categories = Category.query.all()
        category_dict = {category.id: category.type for category in categories}

        # check the len, if no categories exist, abort the request and
        # handle it.
        if len(categories) == 0:
            abort(404)

        return jsonify({
          "success": True,
          "categories": category_dict
        })

    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        paged_questions = pagination(request, questions)
        if(len(paged_questions) == 0):
            abort(404)

        categories = Category.query.all()
        category_dict = [category.type for category in categories]
        return jsonify({
          "success": True,
          "questions": paged_questions,
          "total_questions": len(questions),
          "categories": category_dict,
          "current_category": None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = Question.query.get(question_id)
            # abort if question is None, (NOT FOUND)
            if question is None:
                abort(404)
            # delete the question
            question.delete()
            questions = Question.query.all()
            # return the current page after deleting the question
            formatted_questions = pagination(request, questions)

            return jsonify({
              "success": True,
              "questions": formatted_questions,
              "deleted": question_id
            })

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():

        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term:
            # search for question
            questions = Question.query.filter(
              Question.question.ilike(f'%{search_term}%')).all()

            if len(questions) == 0:
                abort(404)

            formatted_questions = pagination(request, questions)
            return jsonify({
              "success": True,
              "questions": formatted_questions,
              "total_questions": len(questions),
              "current_category": None
            }), 200

        else:

            question_text = body.get('question', None)
            answer = body.get('answer', None)
            category = body.get('category', None)
            difficulty = body.get('difficulty', None)

            # if one of the values is None, abort the request as (BAD REQUEST)
            if ((question_text is None) or (answer is None) or
               (category is None) or (difficulty is None)):
                abort(400)

            # create the question and insert it in the table
            question = Question(question_text, answer, category, difficulty)
            question.insert()

            # paginate the current page
            questions = Question.query.all()
            formatted_questions = pagination(request, questions)

            return jsonify({
              'success': True,
              'questions': formatted_questions,
              'created': question.id,
              'question_created': question.question,
              'total_questions': len(questions)
            }), 200

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        # get all the questions by category
        questions = Question.query.filter(Question.category ==
                                          str(category_id)).all()

        formatted_questions = pagination(request, questions)

        # abort with 404 if no questions by that category or he
        # enter page that does not exist
        if len(formatted_questions) == 0:
            abort(404)

        return jsonify({
          "success": True,
          "questions": formatted_questions,
          "current_category": category_id,
          "total_questions": len(questions)
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        body = request.get_json()

        if not ('quiz_category' in body and 'previous_questions' in body):
            # rise a BAD REQUEST, if one of the values are NONE
            abort(400)

        # getting the previous questions and the category
        category_type = body.get('quiz_category')['id']
        previous_questions = body.get('previous_questions')
        category_questions = []

        if category_type == 0:
            # get all category
            category_questions = Question.query.all()
        else:
            # getting the all questions of the requested category
            category_questions = Question.query.filter(
              Question.category == str(category_type)).all()

        # abort if this category does not have questions
        if len(category_questions) == 0:
            abort(404)

        def new_questions_filter(previous_questions, all_questions):
            # this method will filter the questions, and get new questions ONLY
            new_questions = []
            for check_question in all_questions:
                its_new = True
                for used_question_id in previous_questions:
                    if check_question.id == used_question_id:
                        its_new = False

                if its_new:
                    new_questions.append(check_question.format())
            return new_questions

        def random_question_generator(new_questions):
            # from new questions, this method will get random questions
            index = random.randint(0, len(new_questions) - 1)
            return new_questions[index]

        new_questions = new_questions_filter(previous_questions,
                                             category_questions)

        if len(new_questions) == 0:
            # This mean he have used all the questions available
            return jsonify({
              "success": True
            })

        random_question = random_question_generator(new_questions)

        return jsonify({
          "success": True,
          "question": random_question
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not Found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
        }), 400

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable request"
        }), 422

    return app
