import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random, sys
from models import setup_db, Question, Category
from pprint import pprint

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app, resources={r'/*': {'origins': '*'}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS')

    return response


  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()

    formatted_categories = {}

    for category in categories:
      formatted_categories[category.id] = category.type

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': formatted_categories,
    })


  def paginate_questions(request, questions):
    page = request.args.get('page', 1, type = int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = page * QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in questions]

    return formatted_questions[start:end]

  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    formatted_questions = paginate_questions(request, questions)
    categories = Category.query.order_by(Category.id).all()
    current_category = Category.query.order_by(Category.id).get(questions[0].category)

    formatted_categories = {}

    for category in categories:
      formatted_categories[category.id] = category.type

    if len(formatted_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(questions),
      'categories': formatted_categories,
      'current_category': current_category.type,
    })


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()

    try:
      if question is None:
        abort(404)
      else:
        question.delete()

        return jsonify({
          'success': True,
        })

    except:
      abort(422)


  @app.route('/questions', methods=['POST'])
  def new_question():
    body = request.get_json()

    try:
      question = Question(
        question = body.get('question', None),
        answer = body.get('answer', None),
        difficulty = body.get('difficulty', None),
        category = body.get('category', None),
      )
      question.insert()

      return jsonify({
        'success': True,
      })

    except:
      abort(422)


  @app.route('/questions/search', methods=['POST'])
  def search():
    body = request.get_json()
    search_query = body.get('searchTerm', None)

    try:
      questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_query))).all()
      questions_formatted = paginate_questions(request, questions)
      current_category = Category.query.order_by(Category.id).get(questions[0].category)

      return jsonify({
        'success': True,
        'questions': questions_formatted,
        'total_questions': len(questions),
        'current_category': current_category.type,
      })

    except:
      abort(422)


  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):

    try:
      questions = Question.query.filter(Question.category == category_id).order_by(Question.category).all()
      questions_formatted = paginate_questions(request, questions)
      current_category = Category.query.order_by(Category.id).get(category_id)

      if current_category is None:
        abort(404)

      return jsonify({
        'success': True,
        'questions': questions_formatted,
        'total_questions': len(questions),
        'current_category': current_category.type,
      })
    except:
      abort(422)


  @app.route('/quizzes', methods=['POST'])
  def play():
    body = request.get_json()
    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)
    category_id = int(quiz_category['id'])

    if category_id is None:
      abort(404)

    try:
      questions = Question.query.order_by(Question.id)

      if category_id != 0:
        questions = questions.filter(Question.category == category_id).all()
      else:
        questions = questions.all()

      random_question = random.choice(questions)

      if len(previous_questions) == len(questions):
        return jsonify({
          'success': True,
          'question': None,
        })

      while random_question.id in previous_questions:
        random_question = random.choice(questions)

      return jsonify({
        'success': True,
        'question': random_question.format(),
      })

    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  return app
