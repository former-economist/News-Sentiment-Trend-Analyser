import json

from requests import Session
from Web_Service.routes import db_input
from app import create_app, database
import models
from scraper_funcs import create_search_string
import unittest


class TestWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_config = {
            'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
            'TESTING': True,
            'SECRET_KEY' : '$SECRET_KEY'
        }
        cls.app = create_app(cls.test_config)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self) -> None:
        database.create_all()
        database.session.commit()
    
    def tearDown(self) -> None:
        database.drop_all()
        database.session.commit()

    def test_register(self):
        json_data_01 = {"username" : "john", "email": "john.email@student.com", "password" : "password", "confirmed-password" : "wrongpassword"}
        post = self.client.post('/authorisation/register', json=json_data_01)
        self.assertEqual(post.status_code, 403)

    def test_post_anonymous_query(self):
        
        json_data_01 = {"topic" : "truss", "blocked-words" : ['leadership', 'brexit'], "token" :"" }
        post = self.client.post('/search/', json=json_data_01)
        self.assertEqual(post.status_code, 201)
        self.assertEqual(post.json, {'message': 'Request Recieved anon'})
        post = self.client.post('/search/', json=json_data_01)
        self.assertEqual(post.status_code, 202)
        self.assertEqual(post.json, {'message': 'Request Acknowleged anon'})
        

        # Test to see if similar query create different query.
        # json_data_02 = {"topic" : "rabbit", "blocked-words" : [], "token" :"" }
        # post = self.client.post('/search/', json=json_data_02)
        # self.assertEqual(post.status_code, 201)
        # self.assertEqual(post.json, 'Request Recieved anon')




if __name__ == "__main__":
    unittest.main()
