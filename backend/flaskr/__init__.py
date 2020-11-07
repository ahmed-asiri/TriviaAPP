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
    formatted_questions = [question.format() for question in questions_list]
    return formatted_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
    )
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories')
  def get_categories():
    
    categories = Category.query.order_by(Category.id).all()
    
    # check the len, if no categories exist, abort the request and handle it.
    if len(categories) == 0:
      abort(404)

    # format the categories in proper way for the front-end.
    formatted_categories = [category.format() for category in categories]

    return jsonify({
      "success": True,
      "categories": categories
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_questions():
    questions = Question.query.all()
    paged_questions = pagination(request, questions)

    if(len(paged_questions) == 0):
      abort(404)
    
    categories = Category.query.all()
    category_dict = [category.type for category in categories]

    return {
      "success": True,
      "questions": paged_questions,
      "total_questions": len(questions),
      "categories": category_dict
    }

  



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_questions(question_id):
    try:
      question = Question.query.get(question_id)
      # abort if question is None, (NOT FOUND)
      if question is None:
        abort(404)
      #delete the question
      question.delete()
      questions = Question.query.all()
      #return the current page after deleting the question
      formatted_questions = pagination(request, questions)

      return jsonify({
        "success": True,
        "questions": formatted_questions,
        "deleted": question_id 
      })
    
    except:
      abort(422)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  I HAVE COMBINED BOTH OF THESES ENDPOINTS INTO ONE
  '''
  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  

  @app.route('/questions', methods=['POST'])
  def create_question():

    

    search_term = request.args.get("searchTerm")
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
        "total_questions": len(questions)
      }), 200

    else:
      # create question
      question_data = request.get_json()

      question_text = question_data.get('question', None)
      answer = question_data.get('answer', None)
      category = question_data.get('category', None)
      difficulty = question_data.get('difficulty', None)

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
        'questions': formatted_questions,
        'total_questions': len(questions)
      }), 200



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<string:category_type>/questions')
  def get_questions_by_category(category_type):
    
    # get all the questions by category
    questions = Question.query.filter(Question.category == category_type).all()

    formatted_questions = pagination(request, questions)

    # abort with 404 if no questions by that category or he enter page that does not exist
    if len(formatted_questions) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "current_category": category_type,
      "total_questions": len(questions)
    })
  
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
  

    request_body = request.get_json()

    # getting the previous questions and the category
    category_type = request_body.get('quiz_category')
    previous_questions = request_body.get('previous_questions')

    if (category_type is None) or (previous_questions is None):
      # rise a BAD REQUEST, if one of the values are NONE
      abort(400)
    
    # getting the all questions of the requested category
    category_questions = Question.query.filter(Question.category == category_type).all()

    # abort if this category does not have questions
    if len(category_questions) == 0:
      abort(404)
    
    # take only the question text for easier camparison
    questions_text = [question['question'] for question in previous_questions]


    def new_questions_filter(previous_questions, all_questions):
      # this method will filter the questions, and get new questions ONLY
      new_questions = []
      for check_question in category_questions:
        its_new = True
        for used_question in questions_text:
          if check_question.question == used_question:
            its_new = False
        
        if its_new:
          new_questions.append(check_question.format())
      return new_questions

    def random_question_generator(new_questions):
      # from new questions, this method will get random questions
      index = random.randint(0, len(new_questions) - 1)
      return new_questions[index]


    new_questions = new_questions_filter(questions_text, category_questions)

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



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

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