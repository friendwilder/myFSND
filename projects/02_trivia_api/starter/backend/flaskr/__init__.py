import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * 10
  end = start + 10
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
      # CORS Headers 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  # @cross_origin()
  def get_categories():
    categories_dict = {}
    data = Category.query.order_by(Category.id).all()
    for category in data:
      categories_dict[category.id] = category.type
    return jsonify({
      'success': True,
      'categories': categories_dict
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
  @app.route('/questions', methods=['GET'])
  def get_questions():
    q = Question.query.order_by(Question.id).all()
    questions = paginate_questions(request, q)
    categories = Category.query.order_by(Category.id).all()
    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type
    total_questions = len(Question.query.all())
    current_category = None
    return jsonify({
      'success': True,
      'categories': categories_dict,
      'questions': questions,
      'total_questions': total_questions,
      'current_category': None
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.get(id)

      if question is None:
        abort(404)
      
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      return jsonify({
        'success': True,
        'deleted': id,
        'questions': current_questions,
        'total_questions' : len(Question.query.all())
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
  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()

    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)
    search_term = body.get('searchTerm', None)

    try:
      if search_term:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term)))
        current_questions = paginate_questions(request, selection)
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
        })
      else:
        new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
        new_question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'created': new_question.id,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
        })

    except:
      abort(422)

    return app


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
  def search_term(term):
    print(term + 'not implemented')

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_category_questions(id):
    selection = Question.query.order_by(Question.id).filter(Question.category==id)
    current_questions = paginate_questions(request, selection)
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all())
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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    