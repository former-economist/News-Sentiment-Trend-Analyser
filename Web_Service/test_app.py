
from app import create_app, database
import models
import unittest


class TestWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_config = {
            'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
            'TESTING': True,
            'SECRET_KEY': '$SECRET_KEY'
        }
        cls.app = create_app(test_config)
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
        # Test registeration denied if passwords do not match.
        json_data_01 = {"username": "john", "email": "john.email@student.com",
                        "password": "password", "confirmed-password": "wrongpassword"}
        post = self.client.post('/authorisation/register', json=json_data_01)
        self.assertEqual(post.status_code, 403)

        # Test registration confirms if passwords do match.
        json_data_02 = {"username": "john", "email": "john.email@student.com",
                        "password": "password", "confirmed-password": "password"}
        post02 = self.client.post('/authorisation/register', json=json_data_02)
        self.assertEqual(post02.status_code, 201)

        # Test registration fails when user already exists with details.
        json_data_02 = {"username": "john", "email": "john.email@student.com",
                        "password": "password", "confirmed-password": "password"}
        post02 = self.client.post('/authorisation/register', json=json_data_02)
        self.assertEqual(post02.status_code, 409)

    def test_login(self):
        # Test login with no authorisation details.
        post_no_auth = self.client.post('/authorisation/login')
        self.assertEqual(post_no_auth.status_code, 401)

        # Test login with unrecognised user details.
        post_with_auth = self.client.post('/authorisation/login', username="john", password="password")
        self.assertEqual(post_with_auth.status_code, 401)

        # Create user
        json_data_01 = {"username": "john", "email": "john.email@student.com",
                        "password": "password", "confirmed-password": "password"}
        post = self.client.post('/authorisation/register', json=json_data_01)
        self.assertEqual(post.status_code, 201)

        # Test for successful login with registered user.
        self.assertEqual(post_with_auth.status_code, 201)

    def test_post_query(self):

        # Post anonymous query.
        json_data_01 = {"topic": "truss", "blocked-words": ['leadership']}
        post01 = self.client.post('/search/', json=json_data_01)
        self.assertEqual(post01.status_code, 201)
        self.assertEqual(post01.json, [
                         {'message': 'Request Recieved', 'query_id': 1, 'topic': 'truss -leadership', 'sentiment': None}])
        post02 = self.client.post('/search/', json=json_data_01)
        self.assertEqual(post02.status_code, 202)
        self.assertEqual(post02.json, [{'message': 'Request acknowledged',
                         'query_id': 1, 'topic': 'truss -leadership', 'sentiment': None}])

        # Test to see if similar input create different query.
        json_data_02 = {"topic": "rabbit", "blocked-words": []}
        post03 = self.client.post('/search/', json=json_data_02)
        self.assertEqual(post03.status_code, 201)
        self.assertEqual(post03.json, [
                         {'message': 'Request Recieved', 'query_id': 2, 'topic': 'rabbit', 'sentiment': None}])

        # registration_json_data = {"username" : "john", "email": "john.email@student.com", "password" : "password", "confirmed-password" : "wrongpassword"}
        # post = self.client.post('/authorisation/register', json=registration_json_data)
        # self.assertEqual(post.status_code, 403)

    def test_get_results():
        

if __name__ == "__main__":
    unittest.main()
