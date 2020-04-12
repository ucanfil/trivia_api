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
    self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    # self.category = {
    #   'type': 'Politics'
    # }

    self.question = {
      'question': 'The beaver is the national emblem of which country?',
      'answer': 'Canada',
      'category': '1',
      'difficulty': 2,
    }

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

  def tearDown(self):
    """Executed after reach test"""
    pass

  def test_get_categories(self):
    res = self.client().get('/categories')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['categories'])

  def test_404_get_categories(self):
    res = self.client().get('/categories/2')

    self.assertEqual(res.status_code, 404)

  def test_get_questions(self):
    res = self.client().get('/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['questions'])
    self.assertTrue(data['total_questions'])
    self.assertTrue(data['categories'])
    self.assertTrue(data['current_category'])

  def test_404_get_questions(self):
    res = self.client().get('/questions?page=1000')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['error'], 404)
    self.assertEqual(data['message'], 'Not found')

  def test_delete_question(self):
    res = self.client().delete('/questions/10')
    data = json.loads(res.data)

    question = Question.query.filter(Question.id == 10).one_or_none()

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(question, None)

  def test_422_delete_question(self):
    res = self.client().delete('/questions/1000')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Unproccesable entity')

  def test_post_questions(self):
    res = self.client().post('/questions', json = self.question)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_422_post_questions(self):
    res = self.client().post('/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Unproccesable entity')

  def test_post_search(self):
    res = self.client().post('/questions/search', json = {'searchTerm': 'title'})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['questions'])
    self.assertEqual(data['total_questions'], 2)
    self.assertTrue(data['current_category'])

  def test_post_search_without_results(self):
    res = self.client().post('/questions/search', json = {'searchTerm': 'hello'})
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['questions'], [])
    self.assertEqual(data['total_questions'], 0)
    self.assertEqual(data['current_category'], '')

  def test_get_questions_by_category(self):
    res = self.client().get('/categories/1/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['total_questions'] > 0)
    self.assertTrue(data['current_category'])

  def test_422_get_questions_by_category(self):
    res = self.client().get('/categories/10/questions')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'Unproccesable entity')

  def test_play(self):
    res = self.client().post('/quizzes', json = {
      'previous_questions': [],
      'quiz_category': {'id': 5, 'type': 'Entertainment'}
    })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['question'])

  def test_play_ended(self):
    res = self.client().post('/quizzes', json = {
      'previous_questions': [2, 4, 6],
      'quiz_category': {'id': 5, 'type': 'Entertainment'}
    })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['question'], None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()